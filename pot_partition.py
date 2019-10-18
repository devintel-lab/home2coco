import os
import argparse


parser = argparse.ArgumentParser(description='Generate a COCO style dataset from the HOME training data folder')
parser.add_argument("--input_dir", type=str, default="input")
parser.add_argument("--out_dir", type=str, default="output")
parser.add_argument("--exp", type=int, default=15)
parser.add_argument("--infer_set", dest='infer_set', action='store_true', default=False)
