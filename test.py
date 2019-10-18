import json
import sys

input_file = sys.argv[1]



with open(input_file, "r") as input:
    data = json.load(input)

for img in data['images']:
    found = None
    for annot in data['annotations']:
        if annot['image_id'] == img['id']:
            found = annot
            print(f"{img['file_name']:40}       ---       {found['bbox']}")

    if found is None:
        print(img)



print()