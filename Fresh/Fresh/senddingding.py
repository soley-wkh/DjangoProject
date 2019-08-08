# -*- coding:utf-8 -*-
"""
    version: 
    author : wkh
    time   : 2019/8/2 10:00
    file   : senddingding.py
    
"""
import json
import requests


def ding_talk():
    url = ""
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
            "atMobiles": []
        },
        "isAtAll": True
    }

    send_data = json.dumps(request_data)
    response = requests.post(url, headers=headers, data=send_data)
    content = response.json()
    print(content)
