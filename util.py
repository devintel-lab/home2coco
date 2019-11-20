import os
import os.path as osp

from PIL import Image
import random
import multiwork
import numpy as np
import copy

from scipy.stats import entropy

pot_map = {
    "yellow": [
        "1501", "1502", "1503",
    ],
    "black": [
        "1504", "1505", "1506",
        "1507", "1508", "1509",
        "1512", "1513", "1515",
        "1516", "1517", "1519",
        "1520", "1521", "1522",
        "1523", "1524",
    ],
    "green": [
        "1510", "1511", "1514",
        "1518", "1525", "1526",
        "1527", "1528", "1529",
        "1530", "1531", "1532",
        "1533", "1534", "1535",
        "1536", "1537", "1538",
        "1539", "1540", "1541"
    ]
}

subj2potcolor = {subj: color for color, sbjgrp in pot_map.items()
                 for subj in sbjgrp}


def make_nopot(labels):
    result = {}
    for img, labs in labels.items():
        new_labels = []
        for l in labs:
            if l[0] == 8:
                continue
            new_labels.append(l)

        if len(new_labels) > 0:
            result[img] = new_labels

    return result


def make_justpot(labels):
    result = {}
    for img, labs in labels.items():
        new_labels = []
        for l in labs:
            if l[0] == 8:
                new_labels.append(l)

        if len(new_labels) > 0:
            result[img] = new_labels

    return result

def make_uniform(imgs, labels, num_iters=2500,
                 sample_size=None):
    """
    Random search optimization of image frame subsamples
    to find a configuration with maximal entropy distribution
    across item types.

    :param imgs: list of image paths
    :param labels: dictionary of labels.txt to list of box annotations
    :param num_iters: number of random samples to check
    :param sample_size: number of final output frames
    :return: list of image paths with maximal entropy
    """
    best = (0, None)

    total_dist = total_toy_dist(labels)
    total_dist.sort(key=lambda x: x[1])

    num_toys = len(total_dist)

    toy_dist = np.zeros((num_toys,))

    if sample_size is None:
        sample_size = total_dist[0][1]

    for epoch in range(num_iters):
        toy_dist *= 0
        random.shuffle(imgs)
        for i in imgs[:sample_size]:
            labs = labels[osp.basename(i).replace(".jpg", ".txt")]
            for l in labs:
                toy_dist[l[0]] += 1

        e = entropy(toy_dist/sum(toy_dist))

        if e > best[0]:
            best = (e, copy.deepcopy(imgs[:sample_size]))
            # print(best[1][:3])

    return best[1]


def total_toy_dist(labels):
    results = {}

    for f, vals in labels.items():
        for v in vals:
            if v[0] not in results:
                results[v[0]] = 1
            else:
                results[v[0]] += 1

    return [(k, v) for k, v in results.items()]


def add_image(annot_dict, img_path, img_id, img_labels, args=None):
    if args.alt_img_root is not None:
        img_path = osp.join(args.alt_img_root, osp.basename(img_path))

    img = Image.open(img_path)
    width, height = img.size
    entry = {
        "id": img_id,
        "license": 4,
        "width": width,
        "height": height,
        "file_name": os.path.basename(img_path)
    }
    annot_dict['images'].append(entry)

    for label in img_labels:
        add_label(annot_dict, img_id, label, entry)


def image_path_to_subjinfo(path):
    p = osp.basename(path)
    p = p.split("_")
    exp = int(p[0].replace("exp", ""))
    id = p[1].replace("subj", "")
    frame = int(p[3].replace("frame", "").replace(".jpg", ""))
    return {
        "exp": exp,
        "date": id[:8],
        "kidID": int(id[8:]),
        "frame": frame,
        "cam": p[2]
    }


def filter_subjects(subjs, images):
    st = multiwork.subject_table()
    st = st.loc[st.subID.isin(subjs)]
    imgs = []
    for i in images:
        info = image_path_to_subjinfo(i)
        if info['kidID'] in st.kidID.values:
            imgs.append(i)
    return imgs


def random_subsample(seq, percent=10):
    random.shuffle(seq)
    return seq[:int(len(seq)*percent/100)]


def add_label(annot_dict, img_id, label, img):
    cat = annot_dict['categories'][label[0]]

    w = img['width']
    h = img['height']
    if '1521_parent_frame_list_img_6901' in img['file_name']:
        print()

    label[2] = label[2] * w
    label[3] = label[3] * h
    label[4] = label[4] * w
    label[5] = label[5] * h

    # convert from center coordinates to edges
    label[2] = label[2] - label[4]/2
    label[3] = label[3] - label[5]/2

    box_w = abs(label[4] - label[2])
    box_h = abs(label[5] - label[3])

    entry = {
        "id": label[1],
        "category_id": cat['id'],
        "iscrowd": 0,
        "image_id": img_id,
        "bbox": label[2:],
        "area": box_w*box_h
    }

    annot_dict['annotations'].append(entry)


def subsample(flist, percent=10):
    if not 0 < percent < 100:
        raise Exception("percent needs to be between 0-100")
    random.shuffle(flist)
    N = int(len(flist)*(float(percent)/100))
    train = flist[N:]
    test = flist[:N]
    return train, test


def read_labels(path):
    labels = {}
    label_id = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):
                labels[file] = []
                with open(os.path.join(root, file), "rU") as input:
                    for line in input:
                        lab = line.strip()
                        lab = lab.split()
                        l = [0]*6
                        if len(lab) == 5:
                            l[0] = int(lab[0])
                            l[1] = label_id
                            l[2] = float(lab[1])
                            l[3] = float(lab[2])
                            l[4] = float(lab[3])
                            l[5] = float(lab[4])
                            if l[2] > 1:
                                print(file)
                            labels[file].append(l)
                            label_id += 1
    return labels


def verify_folder(path):
    if not os.path.exists(os.path.join(path, "training.txt")):
        raise Exception(
            "missing training.txt file in the folder\n\ndir: {}".format(path))
    if not os.path.isdir(os.path.join(path, "JPEGImages")):
        raise Exception(
            "missing the JPEGImages folder\n\ndir: {}".format(path))
    if not os.path.isdir(os.path.join(path, "labels")):
        raise Exception("missing the labels folder\n\ndir: {}".format(path))


def filter_no_pot(labels, images):
    results = []
    for img, annots in labels.items():
        if not any(x[0] == 8 for x in annots):
            results.append(img.replace(".txt", ""))

    imgs = [x for x in images if any(y in x for y in results)]
    return imgs


def remove_negative_samples(annots):
    num_img = len(annots['images'])
    imgs_with_annots = []
    for a in annots['annotations']:
        imgs_with_annots.append(a['image_id'])

    imgs_with_annots = set(imgs_with_annots)
    newimgs = [x for x in annots['images'] if x['id'] in imgs_with_annots]
    annots['images'] = newimgs
    return annots


def verify_image_roots(imgs, real_root):
    print()


def template(exp_num):
    return {
        "info": {
            "description": "HOME experiment {}".format(exp_num),
            "url": "TODO",
            "version": "1.0",
            "year": "2019",
            "date_created": "04/01/2019"
        },
        "licenses": [
            {
                "url": "http://creativecommons.org/licenses/by/2.0",
                "id": 4,
                "name": "Attribution License"
            }
        ],
        "images": [],
        "annotations": [],
        "categories": [
            {
                "supercategory": "animal",
                "id": 1,
                "name": "bison"
            },
            {
                "supercategory": "animal",
                "id": 2,
                "name": "alligator"
            },
            {
                "supercategory": "outdoor",
                "id": 3,
                "name": "drop"
            },
            {
                "supercategory": "kitchen",
                "id": 4,
                "name": "kettle"
            },
            {
                "supercategory": "animal",
                "id": 5,
                "name": "koala"
            },
            {
                "supercategory": "food",
                "id": 6,
                "name": "lemon"
            },
            {
                "supercategory": "food",
                "id": 7,
                "name": "mango"
            },
            {
                "supercategory": "animal",
                "id": 8,
                "name": "moose"
            },
            {
                "supercategory": "kitchen",
                "id": 9,
                "name": "pot"
            },
            {
                "supercategory": "animal",
                "id": 10,
                "name": "seal"
            },
        ]
    }
