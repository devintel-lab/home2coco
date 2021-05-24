import os
import sys
import random
import os.path as osp


def subsample(flist, percent=0.1):
    random.shuffle(flist)
    N = int(len(flist)*percent)
    train = flist[N:]
    test = flist[:N]
    return train, test

def read_flist(path):
    results = []
    with open(path, "r") as input:
        for line in input:
            results.append(line)
    return results

if __name__ == "__main__":

    annot_input_dir = sys.argv[1]
    out_dir = sys.argv[2]

    flist = read_flist(osp.join(annot_input_dir, "training.txt"))

    train, test = subsample(flist)


    print()