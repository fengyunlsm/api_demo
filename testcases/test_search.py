# -*- coding:utf-8 _*-
""" 
@author:mongo
@time: 2018/12/17 
@email:3126972006@qq.com
@function： 
"""

import unittest,json, jsonpath

from common import contants
from common import context
from common import logger
from common.context import Context
from common.do_excel import DoExcel
from common.mysql import MysqlUtil
from common.request import Request
from libext.ddtnew import ddt, data


logger = logger.get_logger(logger_name='search')


@ddt
class SearchTest(unittest.TestCase):
    do_excel = DoExcel(contants.case_file)  # 传入cases.xlsx
    cases = do_excel.get_cases('search')

    @classmethod
    def setUpClass(cls): # 每个测试类里面去运行的操作放到类方法里面
        logger.info("初始化测试")
        cls.request = Request()  # 实例化对象

    def setUp(self):  # 每个测试方法里面去运行的操作放到类方法里面
        logger.info("这是一个setUP")


    @data(*cases)
    def test_search(self, case):
        logger.info("开始执行第{0}用例".format(case.id))
        resp = self.request.request(case.method, case.url, case.data, case.cookie)
        resp_obj = json.loads(resp.text)
        expected_obj = json.loads(case.expected)
        expected_data = case.expected_data
        actual_data = case.actual_data

        actual_result = jsonpath.jsonpath(resp_obj, actual_data)
        expected_result = jsonpath.jsonpath(expected_obj, expected_data)
        logger.info("resp_actual: {}, expected: {}".format(actual_result, expected_result))
    



        try:
            # 比较价格是否降序排序
            # 先拿到销量存放起来
            self.assertEqual(expected_result, actual_result, "modified sex error ")  # 断言状态码
            if case.id == 1:
                sales_json = "$..sales"
                sales = jsonpath.jsonpath(resp_obj, sales_json)
                logger.info("sales: {}".format(sales))
                self.assertTrue(sales[0]>=sales[1], "销量降序有误")
                self.assertTrue(sales[1]>=sales[2], "销量降序有误")
            if case.id == 2:
                time_json = "$..createDate"
                time = jsonpath.jsonpath(resp_obj, time_json)
                logger.info("time: {}".format(time))
                self.assertTrue(time[0]>=time[1], "时间降序有误")
                self.assertTrue(time[1]>=time[2], "时间降序有误")
            if case.id == 3 or case.id == 4:
                price_json = "$..price"
                price = jsonpath.jsonpath(resp_obj, price_json)
                logger.info("price: {}".format(price))
                if case.id == 3:
                    self.assertTrue(price[0]>=price[1], "价格降序有误")
                    self.assertTrue(price[1]>=price[2], "价格降序有误")
                if case.id == 4:
                    self.assertTrue(price[0]<=price[1], "价格升序有误")
                    self.assertTrue(price[0]<=price[1], "价格升序有误")
            self.do_excel.write_result('personal_info',case.id + 1, resp.text, 'PASS')
            logger.info("第{}用例执行结果：PASS".format(case.id))
        except AssertionError as e:
            self.do_excel.write_result('personal_info',case.id + 1, resp.text, 'FAIL')
            logger.error("第{}用例执行结果：FAIL".format(case.id))
            raise e



        
