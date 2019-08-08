# -*- coding:utf-8 -*-
"""
    version: 
    author : wkh
    time   : 2019/8/1 20:09
    file   : tasks.py
    
"""
from __future__ import absolute_import
from Fresh.celery import app

import json
import requests


@app.task
def taskExample():
    print('send email ok')


@app.task
def add(x=1, y=2):
    return x + y


@app.task
def ding_talk():
    url = "https://oapi.dingtalk.com/robot/send?access_token=54ae8e937e40a8094cdbaaf17b19ce169d3bd29505e2071d2b6846173176dca3"
    headers = {
        "Content-Type": "application/json",
        "Charset": "utf-8"
    }
    request_data = {
        "msgtype": 'text',
        "text": {
            "content": "I'm at home tonight,let's happy"
        },
        "at": {
            "atMobiles": [],
        },
        "isAtAll": True
    }

    send_data = json.dumps(request_data)
    response = requests.post(url, headers=headers, data=send_data)
    content = response.json()
    print(content)
