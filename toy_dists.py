import os.path as osp
import argparse
import util
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


CATEGORIES = ["bison", "alligator", "drop", "kettle",
              "koala", "lemon", "mango", "moose", "pot",
              "seal"]


def main(args):
    labels = util.read_labels(osp.join(args.input_dir, "labels"))

    total_dist = util.total_toy_dist(labels)
    total_dist.sort(key=lambda x: x[0])

    dist = [(CATEGORIES[i-1], n) for (i, n) in total_dist]

    df = pd.DataFrame(data=dist, columns=["toy", "num_instances"])

    ax = sns.barplot(x="toy", y="num_instances", data=df)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Toy")
    plt.ylabel('Number of Instances')
    plt.title(f'Distribution of Toy Instances')
    plt.tight_layout()
    plt.savefig(osp.join(args.out_dir, "toy_dist.png"), dpi=250)
    plt.close()

    print(args)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_dir", type=str, default="input")  # path to directory with JPEGImages, labels, and training.txt
    parser.add_argument("--out_dir", type=str, default="output") # path to output for plots
    args = parser.parse_args()

    main(args)


