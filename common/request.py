# -*- coding:utf-8 _*-
""" 
@author:mongo
@time: 2018/12/17 
@email:3126972006@qq.com
@function： Requests封装类，使用一个方法解决多种请求方式的调用
"""

import requests, json

from common import logger
from common.config import ReadConfig
from common.handle_cookie import write_cookie, get_cookie_value

logger = logger.get_logger('request')


class Request:

    def __init__(self):
        self.session = requests.sessions.session()  # 实例化一个session

    def request(self, method, url, data=None, cookie=None):
        method = method.upper()  # 将字符转成全部大写
        config = ReadConfig()
        pre_url = config.get('api', 'prod_url')  # 拼接
        url = pre_url + url  # URL拼接
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Referer": "http://eshop.tslj.cn/"
        }
        if data is not None and type(data) == str:
            data = eval(data)  # 如果是字符串就转成字典
        logger.info('method: {0}  url: {1}'.format(method, url))
        logger.info('data: {0}'.format(data))
        logger.info('cookie: {}'.format(cookie))
        
        if method == 'GET':
            resp = self.session.request(method, url=url, params=data, cookies=None)  # 调用get方法，使用params传参
            # logger.info('response: {0}'.format(resp.text))
            return resp

        elif method == 'POST':
            data = json.dumps(data)
            
            if cookie == 'write':
                resp = self.session.request(method, url=url, data=data, headers=headers, cookies=None)
                cookie_dict = requests.utils.dict_from_cookiejar(resp.cookies)
                logger.error("cookie_dict: {}".format(cookie_dict))
                write_cookie(cookie_dict, "web")
            elif cookie == 'yes':
                cookie_dict = get_cookie_value("web")
                cookie_str = "SESSION={}".format(cookie_dict["SESSION"])
                headers['Cookie'] = cookie_str
                logger.info('headers: {}'.format(headers))
                resp = self.session.request(method, url=url, data=data, headers=headers, cookies=cookie_dict)
            elif cookie == 'no':
                resp = self.session.request(method, url=url, data=data, headers=headers, cookies=None)
            else:
                logger.exception("cookie 值有误")
            logger.info('response: {0}'.format(resp.text))
            return resp
        elif method == 'PUT':
            # 修改信息
            if cookie == 'write':
                resp = self.session.request(method, url=url, data=data, headers=headers, cookies=None)
                cookie_dict = requests.utils.dict_from_cookiejar(resp.cookies)
                write_cookie(cookie_dict, "web")
            elif cookie == 'yes':
                cookie_dict = get_cookie_value("web")
                cookie_str = "SESSION={}".format(cookie_dict["SESSION"])
                headers['Cookie'] = cookie_str
                logger.info('headers: {}'.format(headers))
                resp = self.session.request(method, url=url, data=json.dumps(data), headers=headers)
            elif cookie == 'no':
                resp = self.session.request(method, url=url, data=data, headers=headers, cookies=None)
            else:
                logger.exception("cookie 值有误")
                # 不同的代码风格实际上是不一样
            logger.info('response: {0}'.format(resp.text))
            return resp
        elif method == 'PATCH':
            if cookie == 'write':
                resp = self.session.request(method, url=url, data=data, headers=headers, cookies=None)
                cookie_dict = requests.utils.dict_from_cookiejar(resp.cookies)
                write_cookie(cookie_dict, "web")
            elif cookie == 'yes':
                cookie_dict = get_cookie_value("web")
                cookie_str = "SESSION={}".format(cookie_dict["SESSION"])
                headers['Cookie'] = cookie_str
                logger.info('headers: {}'.format(headers))
                resp = self.session.request(method, url=url, data=json.dumps(data), headers=headers)
            elif cookie == 'no':
                resp = self.session.request(method, url=url, data=data, headers=headers, cookies=None)
            else:
                logger.exception("cookie 值有误")
                # 不同的代码风格实际上是不一样
            logger.info('response: {0}'.format(resp.text))
            return resp
        elif method == "DELETE":
            if cookie == 'write':
                resp = self.session.request(method, url=url, data=data, headers=headers, cookies=None)
                cookie_dict = requests.utils.dict_from_cookiejar(resp.cookies)
                write_cookie(cookie_dict, "web")
            elif cookie == 'yes':
                cookie_dict = get_cookie_value("web")
                cookie_str = "SESSION={}".format(cookie_dict["SESSION"])
                headers['Cookie'] = cookie_str
                logger.info('headers: {}'.format(headers))
                resp = self.session.request(method, url=url, data=json.dumps(data), headers=headers)
            elif cookie == 'no':
                resp = self.session.request(method, url=url, data=data, headers=headers, cookies=None)
            else:
                logger.exception("cookie 值有误")
                # 不同的代码风格实际上是不一样
            logger.info('response: {0}'.format(resp.text))
            return resp

        else:
            logger.error('Un-support method !!!')
            pass

    def close(self):
        self.session.close()  # 关闭session

