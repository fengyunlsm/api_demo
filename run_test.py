# -*- coding:utf-8 _*-
""" 
@author:mongo
@time: 2018/12/17 
@email:3126972006@qq.com
@function： 
"""
import unittest

from libext import HTMLTestRunnerNew
from common.config import ReadConfig
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

import smtplib, os, time, platform

from common import contants
config = ReadConfig()
# from testcases.test_login import LoginTest
# from testcases import test_register
# suite = unittest.TestSuite()  # 测试用例集合
# loader = unittest.TestLoader()  # 加载用例
# suite.addTest(loader.loadTestsFromTestCase(LoginTest))
# suite.addTest(loader.loadTestsFromModule(test_register))

# 自动查找testcases目录下，以test开头的.py文件里面的测试类


def new_report(testreport):
    lists = os.listdir(testreport)
    # sysstr = platform.system()
    # if ("Windows" in sysstr):
    #     lists.sort(key=lambda fn:os.path.getmtime(testreport+'\\'+fn)) #获取一个文件中的最近访问时间的文件
    # else:
    lists.sort(key=lambda fn:os.path.getmtime(testreport+'/'+fn))
    file_new = os.path.join(testreport,lists[-1]) 
    print("==========获取最近时间生成的报告文件路径===========> " + file_new)
    return file_new


def send_mail(new_report, filename):
    sender = config.get("email","sender") #读取配置文件中发件人
    sendpwd = config.get("email","mail_pass") #读取配置文件中发件人密码
    receiver = config.get("email","receiver") #读取配置文件中收件人
    print (new_report)

    f = open(new_report,'rb') #获取报告文件
    body_main = f.read()
    f.close()

    # 邮件标题
    msg = MIMEMultipart()
    msg['Subject'] = Header('接口自动化测试报告','utf-8').encode()
    msg['From'] = sender
    msg['To'] = receiver
    msg['date'] = time.strftime("%a,%d %b %Y %H:%M:%S %z")

    #邮件正文
    # html = MIMEText(body_main, 'html', 'utf-8')
    # msg.attach(html)

    # 附件
    att = MIMEText(body_main, 'base64', 'utf-8')
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = 'attachment; filename="report.html"'
    # att.add_header('content-Disposition', 'attachment', filename='report.html')
    msg.attach(att)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(config.get("email","mail_host"))
        smtp.login(sender, sendpwd)
    except:
        smtp = smtplib.SMTP_SSL(config.get("email","mail_host"), config.get("email","port"))
        smtp.login(sender, sendpwd)
    finally:
        smtp.sendmail(sender, receiver.split(","), msg.as_string())       
        print('mail has been send successfully')
        smtp.quit()

discover = unittest.defaultTestLoader.discover(contants.testcases_dir, pattern="test_login.py", top_level_dir=None)

with open(contants.reports_html, 'wb+') as file:
    print (discover)
    # 执行用例
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file,
                                              title='API',
                                              description='API测试报告',
                                              tester='lishaoming')
    runner.run(discover)  # 执行查找到的用例

# 执行发送邮件
report_a = new_report(contants.reports_dir)
send_mail(report_a, contants.reports_html)