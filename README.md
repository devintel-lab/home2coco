# home2coco

convert YOLO training format to COCO dataset format



## usage

```
$ python home2coco.py /path/to/train/dir output_dir exp_num
```

The ```/path/to/train/dir``` is the folder where Sven's ```create_training_data_from_annotations.m``` script outputs the training files. This folder should contain 2 subfolders: ```JPEGImages``` and ```labels```, and 1 ```training.txt``` file.

The ```output_dir``` argument is the path to a folder where this script can dump its outputs.

The ```exp_num``` is the lab internal experiment number, for example the first HOME experiment = 15.