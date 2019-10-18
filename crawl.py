import os
import os.path as osp
from shutil import copy
import sys
import argparse

# expNum_subj_cam_frameNum
#
# e.g.:
#
#       exp15_subj2018121321827_cam07_frame000000033.jpg
template = "exp{}_subj{}_cam{}_frame{:09d}.jpg"


def crawl(path, exp):
    frame_dirs = ("cam07_frames_p", "cam08_frames_p")
    outfiles = []
    for root, dirs, files in os.walk(path):
        if "included" in root:
            if any(x in root for x in frame_dirs):
                cam = "07" if "cam07" in root else "08"
                subj = osp.basename(osp.dirname(root)).replace("_", "")
                for file in files:
                    if file.endswith((".jpg", ".jpeg")):
                        frame_num = file.replace("img_", "").replace(".jpg", "").replace(".jpeg", "")
                        new_name = template.format(exp, subj, cam, int(frame_num))
                        outpath = osp.join(out_dir, "JPEGImages", new_name)
                        outfiles.append(outpath)
                        copy(osp.join(root, file), outpath)
                        if len(outfiles) % 1000 == 0:
                            print(f"file_num: {len(outfiles)}\tcurr_file: {outpath}")
                        # print()

    return outfiles


def write_filelist(files, path):
    with open(path, "w") as out:
        for f in files:
            out.write(f+"\n")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Crawl multiwork and pull the child+parent frames')
    parser.add_argument("--exp_dir", type=str, default="input")
    parser.add_argument("--out_dir", type=str, default="output")
    parser.add_argument("--exp", type=int, default=15)

    args = parser.parse_args()

    exp_dir = args.exp_dir
    out_dir = args.out_dir
    exp = sys.argv[3]

    outfiles = crawl(exp_dir, exp)

    write_filelist(outfiles,osp.join(out_dir, "training.txt"))
