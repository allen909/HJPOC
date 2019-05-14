#coding:utf-8
#__author__:allen909
#__email__:warmeng_git@163.com


import sys
from lib.parse.cmdline import start



# Don't write pyc
sys.dont_write_bytecode = True

# Python version check
try:
    __import__("lib.utils.version")
except ImportError:
    exit("[-] Wrong installation detected (missing modules)!")

if __name__=='__main__':
    start()