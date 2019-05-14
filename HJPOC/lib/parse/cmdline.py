#coding:utf-8
#__author__:allen909
#__email__:warmeng_git@163.com

import os
import argparse
import sys
from lib.core.setting import DESCRIPTION
from lib.utils.output import banner
from lib.core.init import initialize
from lib.core.data import paths
from lib.core.core import normal


def arg_set(parser):

    base = parser.add_argument_group("功能选择")
    base_target_group = base.add_mutually_exclusive_group()
    base_target_group.add_argument("-S", "--info",metavar="APIengine" ,type=str, default=None,help="******************   信息收集",choices=["search","fofa"])
    base_target_group.add_argument("-A", "--attack",metavar="AttackScript" ,type=str, default=None,help="******************   攻击验证")


    module = parser.add_argument_group("模块条件")
    module.add_argument("-u", "--target_simple",metavar="Target" ,type=str, default=None,help="******************   单目标扫描")
    module.add_argument("-k","--key",metavar="keywords", type=str, default=None,help="******************   API引擎关键词")
    module.add_argument("-t", "--thread", type=int, help="******************   配置线程数量 e.g. 100", default=10 ,action="store")





    other = parser.add_argument_group("其他")
    #other.add_argument("-tS", "--task_show",  metavar="TaskID", type=str, default=None,help= "Show task (e.g. all,c81fc4f8f9ab1902)")
    other.add_argument("-d", "--debug", action='store_true', help="******************   显示调试信息", default=False)
    other.add_argument("-o", "--out", type=str, help="******************   文件输出", default=None)


    return parser

def handle(parser):
    banner()
    args = parser.parse_args()
    paths.ROOT_PATH  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    initialize(args)
    if len(sys.argv) == 1:
        sys.argv.append("-h")
        parser.parse_args()
    else:
        normal(args)
        #print('123')


def start():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser = arg_set(parser)
    handle(parser)