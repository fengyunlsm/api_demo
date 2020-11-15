# -*- coding:utf-8 _*-
""" 
@author:mongo
@time: 2018/12/17 
@email:3126972006@qq.com
@function： 
"""

import requests

url = "http://eshop.tslj.cn/issec/settlement/settlement/v1/neworder/campain"

payload = "{\r\n    \"addressId\": \"25e7e7f5e28c433698fdb8f03373b0a6\",\r\n    \"remark\": \"\",\r\n    \"discountcodeList\": [],\r\n    \"couponList\": [],\r\n    \"operator\": \"\"\r\n}"
headers = {
  'Content-Type': 'application/json',
  'Cookie': 'SESSION=c6143faf-8cde-4a4b-a167-05bea3e541a5'
}

response = requests.request("PATCH", url, headers=headers, data = payload)

print(response.text.encode('utf8'))


import pymysql
db = pymysql.connect(host="", user="", password="", daatbase="", charset="utf-8")
cursor = db.cursor()
sql = ""
try:
  cursor.execute(sql)
  # 提交事务
  db.commit()
except Exception as e:
  db.rollback()
# 关闭光标对象
cursor.close()
# 关闭数据库连接
db.close()
