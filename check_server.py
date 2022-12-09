# encoding: utf-8
import socket
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
import io
import telegram
import requests

from fake_useragent import UserAgent
user_agent = UserAgent()

bot = telegram.Bot(token='你的机器人token')
chat_id = '群组的ID'

def get_ip_status(ip,port):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        server.connect((ip,port))
        return True
    except Exception as e:
        return False
    finally:
        server.close()

def send_telegram(content):
    bot.send_message(chat_id=chat_id, text=str(content))


def send_mail(content):
    mail_host="smtp.gmail.com"
    mail_user="谷歌邮箱账号"
    mail_pass="谷歌邮箱密码"
    sub = time.strftime("%Y-%m-%d", time.localtime())

    me = 'XT'
    msg = MIMEText(content, _subtype='plain')
    msg['Subject'] = sub + 'Check somethings'
    msg['From'] = Header("user", 'utf-8')
    msg['To'] = Header("Hello,My boss", 'utf-8')
    mail_res=["123456@qq.com", "接受结果的邮箱"]
    s = smtplib.SMTP(mail_host,25)
    s.starttls()
    s.login(mail_user, mail_pass)
    s.sendmail(me, mail_res, msg.as_string())
    s.close()

def main():
    message = ""
    with open("/root/work/ip_port.txt", "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            ip = line.split(':')[0]
            port = int(line.split(':')[1])
            if(get_ip_status(ip,port)):
                pass
            else:
                print("Hello!!!!!! {} Eror ".format(str(ip)[4:]))
                message += "Hello!!!!!! {} Eror ".format(str(ip)[4:])
    if(len(message)>4):
        bot.send_message(chat_id=chat_id, text='@你的飞机号码提醒 \n出问题了，快来看看')
        send_telegram("【检查服务器:】\nSorry:"+message)
        send_mail(message)
    else:
        send_telegram("【检查服务器:】\n全部正常,有木有很开心?")
        send_mail("It's a good time!")

def check_domain(domain):
    url = 'http://'+domain
    ua = 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'
    #headers = {'User-Agent': user_agent.random,'Accept-Language': 'zh-CN,zh;q=0.9'}
    headers = {'User-Agent': ua}
    req = requests.get(url,headers=headers,timeout=20)
    # print('now domain is '+url)
    return req.status_code

def check_web():
    error_list=[]
    text = '【检查域名】:\n'
    with open("/root/work/domains.txt", "r") as f:
        for line in f.readlines():
            domain = line.strip('\n')
            try:
                status_code = check_domain(str(domain).strip())
            except:
                text +='注意<a href="http://'+domain+'">'+domain+'</a>.请求时间超过了20秒还没响应\n'
                error_list.append(domain)
                continue
            if status_code == 200:
                pass
            else:
                text +='注意<a href="http://'+domain+'">'+domain+'</a>.的错误状态码是'+str(status_code)+'\n'
                error_list.append(domain)
    if(len(error_list)>0):
        bot.send_message(chat_id=chat_id, text='@你的飞机号码提醒 可以多个 \n出问题了，快来看看')
        bot.send_message(chat_id=chat_id,text=text,parse_mode=telegram.ParseMode.HTML)
    else:
        text +='网站检测一切正常。。。'
        bot.send_message(chat_id=chat_id, text=str(text))

if __name__ == '__main__':
    main()
    check_web()
