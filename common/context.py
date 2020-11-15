# -*- coding:utf-8 _*-
""" 
@author:mongo
@time: 2018/12/17 
@email:3126972006@qq.com
@function： 
"""
import re, os, sys

# s 是目标字符串
# d 是替换的内容
# 找到目标字符串里面的标识符KEY，去d里面拿到替换的值
# 替换到s 里面去，然后再返回
base_path = os.getcwd()
sys.path.append(base_path)
from common.config import ReadConfig

config = ReadConfig()


class Context:  # 上下文，数据的准备和记录
    # admin_user = config.get('data', 'admin_user')
    # admin_pwd = config.get('data', 'admin_pwd')
    # loan_member_id = config.get('data', 'loan_member_id')
    # normal_user = config.get('data', 'normal_user')
    # normal_pwd = config.get('data', 'normal_pwd')
    # normal_member_id = config.get('data', 'normal_member_id')
    admin_user = "root"
    admin_pwd = "123456"
    mobile = config.get('data', 'mobile')
    password = config.get('data', 'password')
    search_keyword = config.get('data', 'search_keyword')


def replace(s, d):
    p="\$\{(.*?)}"  # 正则表达式
    while re.search(p, s):
        m = re.search(p, s)
        key = m.group(1)
        value = d[key]
        s = re.sub(p, value, s, count=1)  # 查找并替换找到的第一个
    return s


def replace_new(s):
    p="\$\{(.*?)}"
    while re.search(p, s):
        m = re.search(p, s) # 扫描整个字符串，并返回第一个成功的匹配
        key = m.group(1)  # 返回一个包含所有小组字符串的元组，从 1 到 所含的小组号。
        if hasattr(Context, key):
            # 判断对象是否有该属性
            value = getattr(Context, key)  # 利用反射动态的获取属性值
            s = re.sub(p, value, s, count=1)  # 用于替换
        else:
            return None  # 或者抛出一个异常，告知没有这个属性
    return s

#s = '["mobilephone":"${admin_user}","pwd":"${admin_pwd}"]'
# data = {"admin_user": "15873171553", "admin_pwd": "123456"}
#
# s = replace(s, data)
# print(s)

#s = replace_new(s)
#print(s)
