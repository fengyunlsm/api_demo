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

logger = logger.get_logger(logger_name='case')


@ddt
class OrderTest(unittest.TestCase):
    do_excel = DoExcel(contants.case_file)  # 传入cases.xlsx
    cases = do_excel.get_cases('order')
    request = Request()  # 实例化对象

    @classmethod
    def setUpClass(cls): # 每个测试类里面去运行的操作放到类方法里面
        logger.info("初始化测试")
        cls.request = Request()  # 实例化对象

    def setUp(self):  # 每个测试方法里面去运行的操作放到类方法里面
        print("这是一个setUP")
        pass

    @data(*cases)
    def test_order(self, case):
        # 登录成功之后，将session 写入到json 当中
        logger.info("开始执行第{0}用例".format(case.id))


        data_new = context.replace_new(case.data)  # Str测试数据
        logger.info("data: {}".format(data_new))
        resp = self.request.request(case.method, case.url, data_new, case.cookie)        

        resp_obj = json.loads(resp.text)
        expected_obj = json.loads(case.expected)
        expected_data = case.expected_data
        actual_data = case.actual_data


        actual_result = jsonpath.jsonpath(resp_obj, actual_data)
        expected_result = jsonpath.jsonpath(expected_obj, expected_data)

        logger.info("resp_actual: {}, expected: {}".format(actual_result, expected_result))

        try:
            self.assertEqual(expected_result, actual_result, "order error ")
            self.do_excel.write_result('order', case.id + 1, resp.text, 'PASS')
            logger.info("第{}用例执行结果：PASS".format(case.id))
        except AssertionError as e:
            self.do_excel.write_result('order', case.id + 1, resp.text, 'FAIL')
            logger.error("第{}用例执行结果：FAIL".format(case.id))
            raise e

        try:    
            if case.id == 2:
                # 拿skuid
                search_keyword = getattr(Context, "search_keyword")
                productId_json = "$.page.datas[?(@.spuName== 'SNOOPY 史努比系列 18K白色黄金钻石吊坠')].defaultSkuId".format(search_keyword)
                logger.info("productId_json: {}".format(productId_json))
                productId = jsonpath.jsonpath(resp_obj, productId_json)[0]
                logger.info("productId: {}".format(productId))
                setattr(Context, "productId", productId)
            if case.id == 4:
                # 拿到8720 下面的 商品数量
                productId = getattr(Context, "productId")
                amount_json = "$.shoppingCartVoNews[0].productItem[?(@.id == '{}')].amount".format(productId)
                amount = jsonpath.jsonpath(resp_obj, amount_json)[0]
                logger.info("amount: {}".format(amount))
                setattr(Context, "quantity", str(amount))
            if case.id == 5:
                address_json = "$.TempOrder[0].address.id"
                address_id = jsonpath.jsonpath(resp_obj, address_json)[0]
                setattr(Context, "address_id", str(address_id))
        except:
            logger.error("第{}用例匹配失败：FAIL".format(case.id))
            raise e


    @classmethod
    def tearDownClass(cls):
        cls.request.close()  # 关闭session
