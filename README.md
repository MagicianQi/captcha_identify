# captcha_identify
同花顺验证码识别:
* 降噪 + 分割 + CNN


# Environment

* Python 3.7.6 | Anaconda, Inc.
* `pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple`

# How to use

    python flask_Server.py .

# others

1.可以用uwsgi增加并发能力，supervisor任务管理。
2.最好将整个服务使用docker部署。
