import os

from PIL import Image
import numpy as np

import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from ara.file_utils import get_files_from_path, get_dirs_from_path

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

train_dir = "/home/tjh/workspace/qishuo/data/Captcha/split/train"
validation_dir = "/home/tjh/workspace/qishuo/data/Captcha/split/val"

total_train = sum([len(get_files_from_path(x)) for x in get_dirs_from_path(train_dir)])
total_val = sum([len(get_files_from_path(x)) for x in get_dirs_from_path(validation_dir)])

batch_size = 128
epochs = 15
IMG_HEIGHT = 36
IMG_WIDTH = 36

labels_dict = {0: '2', 1: '3', 2: '4', 3: '6', 4: '7', 5: '8', 6: '9', 7: 'a', 8: 'b', 9: 'c', 10: 'd', 11: 'e', 12: 'f', 13: 'g', 14: 'h', 15: 'i', 16: 'j', 17: 'm', 18: 'n', 19: 'p', 20: 'q', 21: 'r', 22: 't', 23: 'u', 24: 'v', 25: 'x', 26: 'y', 27: 'z'}

model = load_model('char.h5')

img_path = "/home/tjh/workspace/qishuo/data/Captcha/split/val/2/G1DhIVqzbb.png"
img = Image.open(img_path)
img = img.resize((IMG_WIDTH, IMG_HEIGHT))
img = img.convert("RGB")
img = np.array(img)
img = img * (1. / 255)
img = np.expand_dims(img, axis=0)

pred = model.predict(img)
pred_indices = np.argmax(pred, axis=1)
print(labels_dict[pred_indices[0]])

