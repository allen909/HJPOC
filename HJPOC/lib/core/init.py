#coding:utf-8
#__author__:allen909
#__email__:warmeng_git@163.com

import os
import sys

from lib.core.data import logger
from lib.core.data import paths
from lib.core.config import load_conf
from lib.core.enums import CUSTOM_LOGGING


def initialize(args):
    if args.debug:
        logger.set_level(CUSTOM_LOGGING.DEBUG)
    set_paths()
    config_parser()


def set_paths():
    try:
        os.path.isdir(paths.ROOT_PATH)
    except UnicodeEncodeError:
        errMsg = "系统不能处理读取中文路径,"
        errMsg += "请将系统移动至英文路径中"
        exit(errMsg)
        raise SystemExit

    logger.debug("路径初始化...")
    paths.LOG_PATH = os.path.join(paths.ROOT_PATH, "log")
    paths.OUTPUT_PATH = os.path.join(paths.ROOT_PATH, "output")
    paths.SCRIPT_PATH = os.path.join(paths.ROOT_PATH, "script")
    paths.SPECIAL_SCRIPT_PATH = os.path.join(paths.ROOT_PATH, "special")
    paths.DICT_PATH = os.path.join(paths.ROOT_PATH, "dict")
    paths.CONFIG_PATH = os.path.join(paths.ROOT_PATH, "conf")
    paths.DATA_PATH = os.path.join(paths.ROOT_PATH, "data")
    paths.TOOL_PATH = os.path.join(paths.ROOT_PATH, "tool")

    for path in paths.values():
        if not any(path.endswith(_) for _ in (".txt", ".xml", ".zip")):
            if not os.path.exists(path):
                os.mkdir(path)



def config_parser():
    path = os.path.join(paths.CONFIG_PATH, "HJPOC.conf")

    load_conf(path)