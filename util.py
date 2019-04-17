import os
from PIL import Image

def add_image(annot_dict, img_path, img_id, img_labels):
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

def add_label(annot_dict, img_id, label, img):
    cat = annot_dict['categories'][label[0]]

    label[2] = label[2]*img['width']
    label[3] = label[3] * img['height']
    label[4] = label[4] * img['width']
    label[5] = label[5] * img['height']

    # print()

    entry = {
        "id": label[1],
        "category_id": cat['id'],
        "iscrowd": 0,
        "image_id": img_id,
        "bbox": label[2:]
    }

    annot_dict['annotations'].append(entry)

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
                            labels[file].append(l)
                            label_id += 1
    return labels


def verify_folder(path):
    if not os.path.exists(os.path.join(path, "training.txt")):
        raise Exception("missing training.txt file in the folder\n\ndir: {}".format(path))
    if not os.path.isdir(os.path.join(path, "JPEGImages")):
        raise Exception("missing the JPEGImages folder\n\ndir: {}".format(path))
    if not os.path.isdir(os.path.join(path, "labels")):
        raise Exception("missing the labels folder\n\ndir: {}".format(path))

def remove_negative_samples(annots):
    num_img = len(annots['images'])
    imgs = []
    for a in annots['annotations']:
        imgs.append(a['image_id'])

    imgs = set(imgs)
    newimgs = [x for x in annots['images'] if x['id'] in imgs]
    annots['images'] = newimgs
    # print()


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