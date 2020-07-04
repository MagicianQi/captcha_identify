# -*- coding: utf-8 -*-

import flask
import json

from backend.captcha_model import CaptchaModel
from utils.image_utils import base64_to_image, download_image

app = flask.Flask(__name__)
captcha = CaptchaModel()


@app.route("/")
def homepage():
    return "Welcome to the Captcha REST API!"


@app.route("/health")
def health_check():
    return "OK"


@app.route("/api/captcha/predict", methods=["POST", "GET"])
def predict():
    res = {
        "code": 200,
        "message": "OK"
    }
    if flask.request.method == "POST":
        try:
            data = flask.request.data.decode('utf-8')
            data = json.loads(data)
            if "imgUrl" in data:
                image_pil = download_image(data["imgUrl"])
                result = captcha.predict(image_pil)
                res.update({"result": result})
            elif "imgBase64" in data:
                image_pil = base64_to_image(data["imgBase64"])
                result = captcha.predict(image_pil)
                res.update({"result": result})
            else:
                res.update({"code": 400, "message": "Bad request."})
            print("response\t{}".format(res))
        except Exception as e:
            print("Error\t{}".format(e))
    return flask.jsonify(res)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
