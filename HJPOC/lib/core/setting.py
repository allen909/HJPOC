#coding:utf-8
#__author__:allen909
#__email__:warmeng_git@163.com

import random
import re
import sys

INDEX_DATABASE = 'storage'

DESCRIPTION = 'HJPOC为团队自使用渗透框架!包含信息采集,漏洞批量利用等功能!'

IS_WIN = True if sys.platform == 'win32' else False

SITE = "http://www.warmeng.com"

VERSION = "1.0.0"

TYPE = "dev" if VERSION.count('.') > 2 and VERSION.split('.')[-1] != '0' else "test"

VERSION_STRING = "HJPOC/%s#%s" % ('.'.join(VERSION.split('.')[:-1]) if VERSION.count('.') > 2 and VERSION.split('.')[-1] == '0' else VERSION, TYPE)

TYPE_COLORS = {"dev": 33, "test": 90, "pip": 34}

TYPE = "dev" if VERSION.count('.') > 2 and VERSION.split('.')[-1] != '0' else "test"


BANNER = """\033[01;33m\
 #     #       # ######  #######  #####  \033[01;37m{\033[01;%dm%s\033[01;37m}\033[01;33m
 #     #       # #     # #     # #     # 
 #     #       # #     # #     # #       
 #######       # ######  #     # #       
 #     # #     # #       #     # #       
 #     # #     # #       #     # #     # 
 #     #  #####  #       #######  #####  \033[0m\033[4;37m%s\033[0m\n                                      
""" % (TYPE_COLORS.get(TYPE, 31), VERSION_STRING.split('/')[-1], SITE)
