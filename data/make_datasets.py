import os
import random

from utils.preprocess import process_img, smartSliceImg


def random_str(length):
    """
    随机字符串
    """
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(length):
        salt += random.choice(chars)
    return salt


if __name__ == "__main__":
    test_data = []
    output_data_path = "/home/tjh/workspace/qishuo/data/Captcha/split"
    with open("/home/tjh/workspace/qishuo/data/Captcha/test_own.txt", "r") as f:
        for line in f.readlines():
            path, label = line.strip().split(" ")
            test_data.append([path, label])

    nums = len(test_data)
    for path, label in test_data:
        splited_imgs = smartSliceImg(process_img(path))
        if len(splited_imgs) == 6:
            print(label)
            for splited, char in zip(splited_imgs, label):
                if os.path.exists("{}/{}".format(output_data_path, char)):
                    pass
                else:
                    os.mkdir("{}/{}".format(output_data_path, char))
                splited.save("{}/{}/{}.png".format(output_data_path, char, random_str(10)))

