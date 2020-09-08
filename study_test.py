import requests
import json

headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "Referer": "http://eshop.tslj.cn/"
}
# data = json.dumps({'loginPassword': '123456', 'mobile': '13710646151', 'type': 0})
# resp = requests.post('http://eshop.tslj.cn/issec/auth/session/', data=data, headers=headers)  # PARAMS url 传参

y = '''{"platformType":"eshop","code":6001,"message":"手机号或密码不能为空","jwtToken":"null","cmappToken":"null","userInfo":"null"} '''
y_obj = json.loads(y)
print("{}".format(y_obj))
# print('请求url',resp.request.url)
# print('请求参数',resp.request.body)
# print('响应码', resp.status_code)
# print('响应信息', resp.text)
# print("响应内容", resp.headers.get("content-Type"))