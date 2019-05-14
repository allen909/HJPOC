#coding:utf-8
#__author__:allen909
#__email__:warmeng_git@163.com

import base64
import requests
import queue
import threading
import time
from lib.core.config import conf
from lib.core.data import logger
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning #去除python InsecureRequestWarning 警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


q = queue.Queue(10)

class FofaAPI():

    def __init__(self):
        self.email = conf['config']['fofa_api']['email']
        self.key = conf['config']['fofa_api']['token']
        self.keywords = conf['key']
        self.base_url = 'https://fofa.so'
        self.search_api_url = '/api/v1/search/all'
        self.login_api_url = '/api/v1/info/my'
        self.proxy = conf['config']['proxy']

    def get_userinfo(self):
        try:
            url = '{url}{api}'.format(url=self.base_url, api=self.login_api_url)
            data = {"email": self.email, 'key': self.key}
            req = requests.get(url,params=data,verify=False)
            code = req.status_code
            if code != 200:
                msg = '连接失败!fofa炸了?账号没有权限?'
                sys.exit(logger.error(msg))
            else:
                print(req.json())
                return req.json()
        except requests.exceptions.ConnectionError:
            error_msg = {"error": True, "errmsg": "请确认网络连接!"}
            return error_msg

    def get_data(self, page=1, fields='host,ip,port'):
        try:
            url = '{url}{api}'.format(url=self.base_url, api=self.search_api_url)
            query_str = self.keywords
            query_str = bytes(query_str, 'utf-8')
            data = {'qbase64': base64.b64encode(query_str), 'email': self.email, 'key': self.key, 'page': page,
                    'fields': fields}
            req = requests.get(url, params=data,proxies = self.proxy, timeout=10)
            return req.json()
        except requests.exceptions.ConnectionError:
            error_msg = {"error": True, "errmsg": "未知错误,buibuibui～～～"}
        return error_msg

def run(page):
    result = []
    search = FofaAPI()
    print('page', page)
    for page in range(1,2):
            try:
                for host, ip in search.get_data(page, "host,ip")['results']:
                    result.append(ip+'-'+host)
            except:
                pass
    if len(result) == 0:
        sys.exit(logger.error('输出错误,请确认输入的关键词!'))
    for res in result:
        print(res)

def producer():
    for i in range(16):
        q.put(i)

def customer():
    while not q.empty():
        page = q.get()
        run(page)

def _fofa():
    p = threading.Thread(target=producer) # 生产者线程
    cCount = 3 # 消费者个数
    cth = [] # 所有的消费者线程
    for i in range(cCount):
        cth.append(threading.Thread(target=customer))
    p.start()
    for c in cth:
        c.start()

    for c in cth:
        c.join()
    p.join()
