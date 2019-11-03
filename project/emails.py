# encoding:utf-8
# import sys
# import codecs
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.application import MIMEApplication 
import random
_user = "760702659@qq.com"
_pwd = "amjupptoaakcbebb"
_to  = "zhaoyu0910@gmail.com"

lists=[]
def get_code(mail):
    #如名字所示Multipart就是分多个部分 # 构造一个MIMEMultipart对象代表邮件本身
    m=random.randrange(1000,9999)
    lists.append(str(m)) 
    msg = MIMEMultipart() 
    msg["Subject"] = "验证信息"
    msg["From"]  = _user 
    msg["To"]   = mail 

    #---这是文字部分--- 
    part = MIMEText("验证码是:"+str(m)) 
    msg.attach(part) 
    s = smtplib.SMTP("smtp.qq.com", timeout=30)#连接smtp邮件服务器,端口默认是25 
    s.login(_user, _pwd)#登陆服务器 
    s.sendmail(_user, mail, msg.as_string())#发送邮件 
    s.close()
    print("success")

# get_code(_to)

def valid_code():
    return lists[-1]

