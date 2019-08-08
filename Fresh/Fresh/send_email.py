# -*- coding:utf-8 -*-
"""
    version: 
    author : wkh
    time   : 2019/8/1 14:52
    file   : send_email.py
    
"""
# from django.core.mail import send_mail
# from django.conf import settings
#
# send_mail(
#     'Subject here',
#     'Here is the message.',
#     settings.EMAIL_FROM,
#     ['626978318@qq.com']
# )


import smtplib  # 登陆邮件服务器，进行邮件发送
from email.mime.text import MIMEText  # 负责构建邮件格式

subject = "Subject here"
content = "Here is the message."
sender = "13792936061@163.com"
recver = """3392279511@qq.com,
215558997@qq.com,
773733859@qq.com,
912575770@qq.com,
1529825704@qq.com,
1307128051@qq.com,
721788741@qq.com,
3303236612@qq.com,
710731910@qq.com,
329688391@qq.com,
626978318@qq.com,
419538402@qq.com,
1637805820@qq.com,
738389368@qq.com,
329688391@qq.com,
1225858108@qq.com,
329688391@qq.com,
1225858108@qq.com"""

password = "python666"

message = MIMEText(content, "plain", "utf-8")
message["Subject"] = subject
message["To"] = recver
message["From"] = sender
html_message = '<h1>,欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/user/active/">http://127.0.0.1:8000/user/active/</a>'


smtp = smtplib.SMTP_SSL("smtp.163.com", 994)
smtp.login(sender, password)
smtp.sendmail(sender, recver.split(",\n"), message.as_string())
smtp.close()
