import scipy.io.matlab as ml
import numpy as np

import os
import os.path as osp
import argparse


salk_multiwork_root = "/marr/multiwork"



def convert(args):
    results = []

    for root, dirs, files in os.walk(args.annot_dir):
        for file in files:
            if file.endswith(".mat"):
                m = ml.loadmat(osp.join(root, file))
                for i, entry in enumerate(m['annotation_data'][0]):
                    new_path = entry[0][0].replace("\\", "/")
                    new_path = new_path.replace("T:multisensory",
                                                salk_multiwork_root)
                    print(new_path)
                    # if new_path.endswith(".jp"):
                    #     print()
                    m['annotation_data'][0][i][0] = new_path
                results.append((file, m))

    return results


def output(args, mat_files):
    for x in mat_files:
        ml.savemat(osp.join(args.output, x[0]), x[1])


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--annot_dir", type=str)
    parser.add_argument("--output", type=str)

    args = parser.parse_args()

    results = convert(args)

    output(args, results)