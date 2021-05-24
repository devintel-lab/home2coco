import os.path as osp
import pandas as pd





def subject_table():
    data = []
    with open(osp.join(osp.dirname(__file__),
                        "subject_table.txt"), "r") as input:
        for line in input:
            if line.strip():
                data.append([int(x) for x in line.strip().split('\t')])
    df = pd.DataFrame(data, columns=["subID", "exp",
                                     "date", "kidID"])
    return df