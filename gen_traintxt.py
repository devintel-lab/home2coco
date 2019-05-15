import os
import sys

input_dir = sys.argv[1]
outpath = sys.argv[2]

paths = []

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith((".jpg", ".jpeg")):
            paths.append(os.path.abspath(os.path.join(root, file)))

with open(outpath, "w") as output:
    output.write("\n".join(paths))