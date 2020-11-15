import requests, json


# 启动任务
# url = "http://admin:111111@182.254.177.49:8080/job/api_demo/build"
# ret = requests.post(url)
# print (ret.text)



# 远程调用jenkins api返回最新任务编号

# url  = "http://admin:111111@182.254.177.49:8080/job/api_demo/lastBuild/buildNumber"
# ret = requests.get(url)
# print (ret.text)


url  = "http://admin:111111@182.254.177.49:8080/job/api_demo/12/api/json"
ret = requests.get(url)
print(json.dumps(ret.json(), indent=2))