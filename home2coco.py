import json
import sys
import os
from scipy.io import matlab

import util

annot_input_dir = sys.argv[1]
output_dir = sys.argv[2]
exp_num = sys.argv[3]
mode = sys.argv[4] # either "train" or "test"

util.verify_folder(annot_input_dir)

image_paths = []
with open(os.path.join(annot_input_dir, "training.txt"), "r") as input:
    for line in input:
        image_paths.append(line.strip())

labels = util.read_labels(os.path.join(annot_input_dir, "labels"))

annot_dict = util.template(exp_num=exp_num)

for img_num, img in enumerate(image_paths):
    fname = os.path.basename(img)
    if os.path.splitext(fname)[0]+".txt" in labels:
        img_labels = labels[os.path.splitext(fname)[0]+".txt"]
    else:
        img_labels = []
    util.add_image(annot_dict, img, img_num, img_labels)

outpath = os.path.join(output_dir, "experiment_{}_coco_{}.json".format(exp_num, mode))

if mode != "test":
    util.remove_negative_samples(annot_dict)

with open(outpath, "w") as out:
    json.dump(annot_dict, out)