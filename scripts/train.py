import os

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from ara.file_utils import get_files_from_path, get_dirs_from_path

# -----------------------全局参数-----------------------

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

train_dir = "/home/tjh/workspace/qishuo/data/Captcha/split/train"
validation_dir = "/home/tjh/workspace/qishuo/data/Captcha/split/val"

total_train = sum([len(get_files_from_path(x)) for x in get_dirs_from_path(train_dir)])
total_val = sum([len(get_files_from_path(x)) for x in get_dirs_from_path(validation_dir)])

batch_size = 128
epochs = 15
IMG_HEIGHT = 36
IMG_WIDTH = 36
num_classes = 28

# -----------------------构造 datasets-----------------------

train_image_generator = ImageDataGenerator(rescale=1. / 255)  # Generator for our training data
validation_image_generator = ImageDataGenerator(rescale=1. / 255)  # Generator for our validation data

train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=train_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode='categorical')

val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                              directory=validation_dir,
                                                              target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                              class_mode='categorical')

# -----------------------标签名字映射-----------------------

labels = train_data_gen.class_indices
labels_dict = dict((v, k) for k, v in labels.items())

# -----------------------模型定义-----------------------

model = Sequential([
    Conv2D(16, 3, padding='same', activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    MaxPooling2D(),
    Conv2D(32, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(num_classes)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()

# -----------------------训练-----------------------

history = model.fit_generator(
    train_data_gen,
    steps_per_epoch=total_train // batch_size,
    epochs=epochs,
    validation_data=val_data_gen,
    validation_steps=total_val // batch_size
)

# -----------------------保存模型-----------------------

model.save('char.h5')
