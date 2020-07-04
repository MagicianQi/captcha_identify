
import io
import json
import base64
import requests

from PIL import Image


def image_to_base64(image):
    if type(image) == "numpy.ndarray":
        image = Image.fromarray(image)
    image_pil = io.BytesIO()
    image.save(image_pil, format='PNG')
    return base64.b64encode(image_pil.getvalue()).decode('utf-8')


if __name__ =="__main__":
    test_img = Image.open("/home/tjh/workspace/qishuo/data/Captcha/imgs/code_img_999877.png")
    test_img_base64 = image_to_base64(test_img)

    post_json = {
        "imgBase64": test_img_base64
    }

    response = requests.post("http://127.0.0.1:8080/api/captcha/predict", data=json.dumps(post_json))
    response.raise_for_status()
    print(response.json())
