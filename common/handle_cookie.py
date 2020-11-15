#coding=utf-8
import sys
import os
import configparser
base_path = os.getcwd()
print (base_path)
sys.path.append(base_path)
import json
from common.handle_json import *

def get_cookie_value(cookie_key):
    '''
    获取cookie
    '''
    data = read_json("/conf/cookie.json")
    return data[cookie_key]


def write_cookie(data,cookie_key):
    '''
    写入cookie
    '''
    data1 = read_json("/conf/cookie.json")
    data1[cookie_key] = data
    write_value(data1)


if __name__ == "__main__":
    data = {
        "aaaa":"1111111111111111"
    }
    print(write_cookie(data,'web'))

