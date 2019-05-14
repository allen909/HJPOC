#coding:utf-8
#__author__:allen909
#__email__:warmeng_git@163.com

from ..core.datatype import AttribDict
from ..core.log import logger

paths = AttribDict()

logger = logger()

engine = None

conf = AttribDict()
#
# object to share within function and classes results
kb = AttribDict()
#
# # object with each database management system specific queries
# # queries = {}