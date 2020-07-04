from tensorflow.keras.models import load_model
import numpy as np

from utils.preprocess import process_img, smartSliceImg


IMG_HEIGHT = 36
IMG_WIDTH = 36

labels_dict = {0: '2', 1: '3', 2: '4', 3: '6', 4: '7', 5: '8', 6: '9', 7: 'a', 8: 'b', 9: 'c', 10: 'd', 11: 'e', 12: 'f', 13: 'g', 14: 'h', 15: 'i', 16: 'j', 17: 'm', 18: 'n', 19: 'p', 20: 'q', 21: 'r', 22: 't', 23: 'u', 24: 'v', 25: 'x', 26: 'y', 27: 'z'}
model = load_model('char.h5')


def clear(img):
    l = []
    # 点降噪
    for x in range(1, img.size[0] - 1):
        for y in range(1, img.size[1] - 1):
            nearDots1 = 0
            L = img.getpixel((x, y))
            if L == img.getpixel((x + 1, y)):
                nearDots1 += 1
            if L == img.getpixel((x - 1, y)):
                nearDots1 += 1
            if L == img.getpixel((x, y + 1)):
                nearDots1 += 1
            if L == img.getpixel((x, y - 1)):
                nearDots1 += 1

            if nearDots1 > 3:
                l.append((x, y))
    for t in l:
        img.putpixel(t, 255)
    return img


def rescale_img(img):
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    img = img.convert("RGB")
    img = np.array(img)
    img = img * (1. / 255)
    img = np.expand_dims(img, axis=0)
    return img


test_data = []
with open("/home/tjh/workspace/qishuo/data/Captcha/test_own.txt", "r") as f:
    for line in f.readlines():
        path, label = line.strip().split(" ")
        test_data.append([path, label])

nums = len(test_data)

i = 0
for path, label in test_data:
    result = ""
    for splited in smartSliceImg(process_img(path)):
        img = clear(splited)
        img = rescale_img(img)
        pred = model.predict(img)
        pred_indices = np.argmax(pred, axis=1)
        t = labels_dict[pred_indices[0]]
        result += t
    print("{}  ====>  {}".format(result, label))
    if label == result:
        i += 1

print("acc: {}".format(i / nums))

