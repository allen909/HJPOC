#coding:utf-8
#__author__:allen909
#__email__:warmeng_git@163.com


import sys
#from lib.utils.output import print_dic
from lib.core.data import logger
from lib.core.data import conf
from lib.core.data import paths

def init_options(args):
    conf.OUT = args.out
    thread_register(args) #线程参数配置
    info_register(args)  #信息收集引擎配置
    key_register(args)  #关键词配置

def key_register(args):
    if args.key:
        if args.info:
            conf['key'] = args.key
            logger.sysinfo("设置语法: %s" % str(args.key))
        else:
            msg = '请先检查是否载入搜索引擎! [-S].'
            sys.exit(logger.error(msg))

def thread_register(args):
    if  not 0 < args.thread < 501:
        msg = '输入的线程数量错误 [-t] , 范围: 1 - 500.'
        sys.exit(logger.error(msg))
    conf['thread_num'] = args.thread
    logger.sysinfo("设置线程数量: %s" % str(conf['thread_num']))

def info_register(args):
    if args.info:
        conf['info'] = args.info
        logger.sysinfo("载入引擎: %s" % (conf['info']))

