import json
import sys


def area(bbox):
    w = abs(bbox[2] - bbox[0])
    h = abs(bbox[3] - bbox[1])
    return w * h

input_file = sys.argv[1]
output = sys.argv[2]


with open(input_file, "r") as input:
    data = json.load(input)

print()

# for i, bbox in enumerate(data['annotations']):
#     a = area(bbox['bbox'])
#     data['annotations'][i]['area'] = a
#
# with open(output, "w") as out:
#     json.dump(data, out)
#
# print()