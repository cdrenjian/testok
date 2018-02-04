import smtplib
from email.mime.text import MIMEText


class Mail(object):
    def __init__(self,sender = 'xipan1994@163.com',receivers = ['302870287@qq.com']):
        #设置服务器所需信息
        #163邮箱服务器地址
        self.mail_host = 'smtp.163.com'
        #163用户名
        self.mail_user = 'xipan1994@163.com'
        #密码(部分邮箱为授权码)
        self.mail_pass = 'tomato123'
        #邮件发送方邮箱地址
        self.sender = sender
        #邮件接受方邮箱地址
        self.receivers = receivers
    def send_mail(self,msg):
        message = MIMEText(msg,'plain','utf-8')
        #邮件主题
        message['Subject'] = '交易系统报告'
        #发送方信息
        message['From'] = self.sender
        #接受方信息
        message['To'] = ','.join(self.receivers)   #多个接收者用 "，"join
        #登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            #连接到服务器
            smtpObj.connect(self.mail_host,25)
            #登录到服务器
            smtpObj.login(self.mail_user,self.mail_pass)
            #发送
            smtpObj.sendmail(self.sender,self.receivers,message.as_string())
            #退出
            smtpObj.quit()
            return True
        except smtplib.SMTPException as e:
            print('error',e) #打印错误
