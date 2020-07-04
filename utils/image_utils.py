# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import io
import base64
import requests

from PIL import Image


def download_image(image_url):
    response = requests.get(image_url)
    response = response.content
    bytes_obj = io.BytesIO(response)
    image = Image.open(bytes_obj)
    image = image.convert("RGB")
    return image


def base64_to_image(image_base64):
    data = base64.b64decode(image_base64)
    image = io.BytesIO(data)
    image = Image.open(image)
    image = image.convert("RGB")
    return image
