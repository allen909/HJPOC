#coding:utf-8
#__author__:allen909
#__email__:warmeng_git@163.com


from lib.core.options import init_options
from lib.core.engine import Engine
from lib.core.data import conf



def normal(args):

    name = '123'
    print(conf.keys())
    init_options(args)
    engine = Engine(name)
    engine.load_targets()


    #engine.run()
