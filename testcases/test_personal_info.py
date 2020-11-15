# -*- coding:utf-8 _*-
""" 
@author:mongo
@time: 2018/12/17 
@email:3126972006@qq.com
@function： 
"""
import unittest, jsonpath
import json

from libext.ddtnew import ddt, data

from common import contants, logger
from common.do_excel import DoExcel
from common.request import Request

logger = logger.get_logger(logger_name='case')


@ddt
class PersonalInfoTest(unittest.TestCase):
    do_excel = DoExcel(contants.case_file)  # 传入cases.xlsx
    personal_info_case = do_excel.get_cases('personal_info')  # 获取登录用例
    request = Request()  # 实例化对象

    def setUp(self):
        # 登录
        pass

    @data(*personal_info_case)
    def test_personal_info(self, case):
        logger.info("开始执行第{}用例".format(case.id))
        resp = self.request.request(case.method, case.url, case.data, case.cookie)
        resp_obj = json.loads(resp.text)
        expected_obj = json.loads(case.expected)
        expected_data = case.expected_data
        actual_data = case.actual_data

        actual_result = jsonpath.jsonpath(resp_obj, actual_data)
        expected_result = jsonpath.jsonpath(expected_obj, expected_data)
        logger.info("resp_actual: {}, expected: {}".format(actual_result, expected_result))

        try:
            self.assertEqual(expected_result, actual_result, "modified sex error ")
            self.do_excel.write_result('personal_info',case.id + 1, resp.text, 'PASS')
            logger.info("第{}用例执行结果：PASS".format(case.id))
        except AssertionError as e:
            self.do_excel.write_result('personal_info',case.id + 1, resp.text, 'FAIL')
            logger.error("第{}用例执行结果：FAIL".format(case.id))
            raise e