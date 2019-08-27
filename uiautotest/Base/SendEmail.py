#coding=utf-8
__author__ = 'zcs'
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
class SendEmail():
    def sendEmail(self,fp):
        smtpserver = 'smtp.163.com'
        username = 'chen1247619686@163.com'
        password='chen11'
        sender='chen1247619686@163.com'
        receiver=['chen1247619686@163.com','1247619686@qq.com','876158355@qq.com','zhangzhiqiang@aspirecn.com']
        subject = 'Pythonemail'
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = 'chen1247619686@163.com <chen1247619686@163.com>'
        #msg['To'] = receiver
        #收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
        msg['To'] = ";".join(receiver)
        #msg['Date']='2012-3-16'

        #构造附件
        sendfile=open(fp,'rb').read()
        text_att = MIMEText(sendfile, 'base64', 'utf-8')
        text_att["Content-Type"] = 'application/octet-stream'
        text_att.add_header('Content-Disposition', 'attachment', filename='jd.htm')
        msg.attach(text_att)

        #发送邮件
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
