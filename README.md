# captcha_identify
同花顺验证码识别:
* 降噪 + 分割 + CNN


# Environment

* Python 3.7.6 | Anaconda, Inc.
* `pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple`

# How to use

    gunicorn --workers=2 --bind=0.0.0.0:8080  flask_server:app

# others

1.最好将整个服务使用docker部署。
