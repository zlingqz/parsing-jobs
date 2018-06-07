# 请求
# URL: http: // fanyi.youdao.com / translate_o?smartresult = dict & smartresult = rule
# http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule
# {"translateResult":[[{"tgt":"test","src":"测试"}]],"errorCode":0,"type":"zh-CHS2en","smartResult":{"entries":["","[试验] test\r\n","measurement\r\n"],"type":1}}

# -*- coding:utf-8 -*-
"""
Created on Sun May 03 09:36:12 2015

@author: 90Zeng
"""

from urllib.request import urlopen
from urllib.parse import urlencode
import json

# 注意这里用unicode编码，否则会显示乱码
content = input(u"请输入要翻译的内容：")
# 网址是Fig6中的 Response URL
url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=http://www.youdao.com/'
url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
# 爬下来的数据 data格式是Fig7中的 Form Data
# data = {}
# data['type'] = 'AUTO'
# data['i'] = content
# data['doctype'] = 'json'
# data['xmlVersion'] = '1.6'
# data['keyfrom'] = 'fanyi.web'
# data['ue'] = 'UTF-8'
# data['typoResult'] = 'true'


data = {}
data['i'] = 'f'
data['from'] = 'AUTO'
data['to'] = 'AUTO'
data['smartresult'] = 'dict'
data['client'] = 'fanyideskweb'
data['salt'] = '1528349312469'
data['sign'] = '1f6203acbf608960ad7450434817fbe7'
data['doctype'] = 'json'
data['version'] = '2.1'
data['keyfrom'] = 'fanyi.web'
data['action'] = 'FY_BY_REALTIME'
data['typoResult'] = 'true'

# 数据编码
data = urlencode(data)

# 按照data的格式从url爬内容
response = urlopen(url, data)
# 将爬到的内容读出到变量字符串html，
html = response.read()
# 将字符串转换成Fig8所示的字典形式
target = json.loads(html)
# 根据Fig8的格式，取出最终的翻译结果
result = target["translateResult"][0][0]['tgt']

# 这里用unicode显示中文，避免乱码
print(u"翻译结果：%s" % (target["translateResult"][0][0]['tgt']))