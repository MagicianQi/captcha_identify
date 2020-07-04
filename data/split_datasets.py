import os
import shutil

from ara.file_utils import get_files_from_path, get_dirs_from_path

splited_data_path = "/home/tjh/workspace/qishuo/data/Captcha/split/data"
train_path = "/home/tjh/workspace/qishuo/data/Captcha/split/train"
val_path = "/home/tjh/workspace/qishuo/data/Captcha/split/val"
rate = 0.8

for char_dir in get_dirs_from_path(splited_data_path):
    name = char_dir.strip().split("/")[-1]
    imgs = get_files_from_path(char_dir)
    print("process: {}".format(name))
    if len(imgs) > 100:
        os.mkdir("{}/{}".format(train_path, name))
        os.mkdir("{}/{}".format(val_path, name))
        for i, img in enumerate(imgs):
            if i < len(imgs) * 0.8:
                shutil.copy(img, "{}/{}".format(train_path, name))
            else:
                shutil.copy(img, "{}/{}".format(val_path, name))
