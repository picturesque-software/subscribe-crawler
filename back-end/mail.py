import smtplib
# smtplib 用于邮件的发信动作
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header
# 用于构建邮件头
import csv
# 引用csv模块，用于读取邮箱信息
import random
 

# 发信方的信息：发信邮箱，QQ邮箱授权码
# 方便起见，你也可以直接赋值
from_addr = '南小宝'
password = ''#授权码需要自己登陆邮箱，进入设置，隐私设置，开启指定的SMTP设置
 
# 发信服务器
smtp_server = 'smtp.qq.com'
 
 
# 读取收件人数据，并启动写信和发信流程
with open('addrs.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        to_addrs=row[1]
        text=row[2];

        #验证码
        #code = random.randint(100000, 999999);
        #构造邮件内容
        #text = '您好，你的南小宝邮箱验证码为: \n' + str(code) + "\n如非您本人操作，请忽略此邮件。\n"

        msg = MIMEText(text,'plain','utf-8')
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addrs)
        msg['Subject'] = Header('python test')
        server = smtplib.SMTP_SSL()
        server.connect(smtp_server, 465)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addrs, msg.as_string())
 
# 关闭服务器
server.quit()
