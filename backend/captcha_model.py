# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from tensorflow.keras.models import load_model

from utils.preprocess import smartSliceImg, process_img, clear, rescale_img
from settings import MODEL_PATH, LABEL_DICT


class CaptchaModel(object):

    def __init__(self,
                 model_path=MODEL_PATH,
                 label_dict=LABEL_DICT):
        self.model = load_model(model_path)
        self.label_dict = label_dict

    def predict(self, image_pil):
        result = ""
        for splited in smartSliceImg(process_img(image_pil)):
            img = clear(splited)
            img = rescale_img(img)
            pred = self.model.predict(img)
            pred_indices = np.argmax(pred, axis=1)
            t = self.label_dict[pred_indices[0]]
            result += t
        return result