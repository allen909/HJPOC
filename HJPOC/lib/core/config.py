#coding:utf-8
#__author__:allen909
#__email__:warmeng_git@163.com

import configparser
from lib.core.data import logger
from lib.core.data import conf

def load_conf(path):
    logger.debug("载入config...")
    cf = configparser.ConfigParser()
    cf.read(path)
    sections = cf.sections()

    configs = {}

    for section in sections:
        logger.debug("载入config: %s" % (section))
        config = {}

        for option in cf.options(section):
            config[option] = cf.get(section,option)

        configs[section] = config
    #print(configs)
    conf['config'] = configs
    conf['config']['basic']['user_agent'] = conf['config']['basic']['user_agent'].split('\n')

#     print(conf['config'])
#     print(conf['config']['basic']['user_agent'])
#
# if __name__ == '__main__':
#
#     load_conf('/Users/nevermore/Desktop/My_Python_Code/wnscqq/conf/wnscqq.conf')
