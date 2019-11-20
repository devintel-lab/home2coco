import json
import sys
import os
import argparse
import copy
from scipy.io import matlab


import util


def generate_annot_dict(exp_num, image_paths, labels, mode, args):
    annot_dict = util.template(exp_num=exp_num)

    for img_num, img in enumerate(image_paths):
        fname = os.path.basename(img)
        if os.path.splitext(fname)[0] + ".txt" in labels:
            img_labels = labels[os.path.splitext(fname)[0] + ".txt"]
        else:
            img_labels = []
        util.add_image(annot_dict, img, img_num, img_labels, args)

    if mode != "inference":
        annot_dict = util.remove_negative_samples(annot_dict)

    return annot_dict


def gen_and_write(output_dir, exp_num, image_paths, labels, mode, tag=None, args=None):
    annot_dict = generate_annot_dict(
        exp_num, image_paths, labels, mode=mode, args=args)
    if tag:
        outpath = os.path.join(
            output_dir, "experiment_{}_coco_{}_{}.json".format(exp_num, mode, tag))
    else:
        outpath = os.path.join(
            output_dir, "experiment_{}_coco_{}.json".format(exp_num, mode))
    with open(outpath, "w") as out:
        json.dump(annot_dict, out)


parser = argparse.ArgumentParser(
    description='Generate a COCO style dataset from the HOME training data folder')
# path to directory with JPEGImages, labels, and training.txt
parser.add_argument("--input_dir", type=str, default="input")
# directory to output the training json file
parser.add_argument("--out_dir", type=str, default="output")
parser.add_argument("--exp", type=int, default=15)  # the experiment
parser.add_argument("--infer_set", dest='infer_set', action='store_true',
                    default=False)  # generate an inference dataset
parser.add_argument("--pot_partition", dest='pot_part', action='store_true',
                    default=False)  # partition datasets by the color of the pot
# list of subjects to subsample
parser.add_argument("--subsamp_subj", nargs='*')
# percentage to random subsample frames
parser.add_argument("--samp_percent", type=int)
parser.add_argument("--tag", type=str, default=None)  # tag to append to output
# run optimization pass to make item distributions uniform
parser.add_argument("--make_uniform", action='store_true', default=False)
# alternate root dir for images
parser.add_argument("--alt_img_root", type=str, default=None)
parser.add_argument("--nopot", action='store_true', default=False)
parser.add_argument("--justpot", action='store_true', default=False)


args = parser.parse_args()

annot_input_dir = args.input_dir
output_dir = args.out_dir
exp_num = args.exp


util.verify_folder(annot_input_dir)





image_paths = []
with open(os.path.join(annot_input_dir, "training.txt"), "r") as input:
    for line in input:
        image_paths.append(line.strip())


labels = util.read_labels(os.path.join(annot_input_dir, "labels"))

if args.infer_set:
    if args.subsamp_subj:
        image_paths = util.filter_subjects(args.subsamp_subj, image_paths)
        image_paths = util.random_subsample(
            image_paths, percent=args.samp_percent)

    gen_and_write(output_dir, exp_num,
                  image_paths, labels,
                  mode="inference",
                  tag=args.tag, args=args)

if args.nopot:
    labels = util.make_nopot(labels)

if args.justpot:
    labels = util.make_justpot(labels)


if args.pot_part:
    partitions = []
    no_pot_imgs = util.filter_no_pot(labels, image_paths)
    for color, subjs in util.pot_map.items():
        subj_imgs = []
        subj_imgs.extend(
            [x for x in image_paths if os.path.basename(x).startswith(tuple(subjs))])
        imgs = list(set(no_pot_imgs + subj_imgs))
        if args.make_uniform:
            imgs = util.make_uniform(imgs, labels)

        train, test = util.subsample(imgs, percent=10)

        partitions.append((color, train, test))

    for p in partitions:
        labels = util.read_labels(os.path.join(annot_input_dir, "labels"))

        gen_and_write(output_dir, exp_num,
                      p[1], labels, mode=f"{p[0]}_train", args=args)
        gen_and_write(output_dir, exp_num,
                      p[2], labels, mode=f"{p[0]}_test", args=args)
        # print()
else:
    train, test = util.subsample(image_paths, percent=10)

    if args.nopot:
        tag = "nopot"
    elif args.justpot:
        tag = "justpot"
    else:
        tag = None

    gen_and_write(output_dir, exp_num, train, labels, mode="train", args=args, tag=tag)
    gen_and_write(output_dir, exp_num, test, labels, mode="test", args=args, tag=tag)
