from email.mime.text import MIMEText
import requests
import datetime
import smtplib
import time

try:
    theip = str(requests.get("http://ip.42.pl/raw").text) 
    theip = ""
    print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"  Running Now")
except:
    theip = ""
    print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"  Running Now, But ERR_CONNECTION_RESET")
while True:
    time.sleep(600) #等待10分钟
    try:
        content = str(requests.get("http://ip.42.pl/raw").text) #获取公网IP
        print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"  Running Now")
    except:
        print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"  Running Now, But ERR_CONNECTION_RESET")
        continue
    if theip == content:
        print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"  IP Address Has Not Changed, And Now IP Address Is  "+theip)
        continue
    theip = content
    message = MIMEText(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"  Now IP Address Is  "+theip,'plain','utf-8') #获取即时时间和IP地址作为邮件内容
    mail_host = 'smtp.163.com'                      #163邮箱服务器地址
    mail_user = '18583757695'                       #163用户名
    mail_pass = 'UPOWDBCSEJKAXYGK'                  #密码(部分邮箱为授权码) 
    sender = '18583757695@163.com'                  #邮件发送方邮箱地址
    receivers = ['1367678130@qq.com']               #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发  
    message['Subject'] = 'Public Network Ip'        #邮件主题     
    message['From'] = sender                        #发送方信息
    message['To'] = receivers[0]                    #接受方信息     

    try:
        smtpObj = smtplib.SMTP()                    #连接到服务器
        smtpObj.connect(mail_host,25)               #登录到服务器smtpObj = smtplib.SMTP_SSL(mail_host)
        smtpObj.login(mail_user,mail_pass)          #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string())   #退出
        smtpObj.quit() 
        print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"  IP Address Changed, The Email Sent Successfully, And Now IP Address Is  "+theip)
    except smtplib.SMTPException as e:
        print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"  IP Address Changed, But For Some Reason The Mail Failed To Send",e)                            #打印错误

# from urllib.request import urlopen
# my_ip = urlopen('http://ip.42.pl/raw').read()
# print('ip.42.pl', my_ip)
 
# from json import load
# from urllib.request import urlopen
 
# my_ip = load(urlopen('http://jsonip.com'))['ip']
# print('jsonip.com', my_ip)
 
# from json import load
# from urllib.request import urlopen
 
# my_ip = load(urlopen('http://httpbin.org/ip'))['origin']
# print('httpbin.org', my_ip)
 
# from json import load
# fromurllib.request import urlopen
 
# my_ip = load(urlopen('https://api.ipify.org/?format=json'))['ip']
# print('api.ipify.org', my_ip)

# strip = requests.get("http://ip.42.pl/raw").text
# while strip != requests.get("http://ip.42.pl/raw").text:
#     print("unsame")
#     time.sleep(10)

# print("unsame")
# time.sleep(10)



