#coding:utf-8
#__author__:allen909
#__email__:warmeng_git@163.com

import queue
import time
import sys
import urllib.parse
import os
import traceback
import threading
import importlib.util
from concurrent.futures import ThreadPoolExecutor
from lib.core.data import conf, logger,paths
#from lib.utils.output import print_dic

#from lib.api.api import search_engine
from lib.api.fofa import _fofa

# from script import init
# from script import curl
# from script import ceye_verify_api
# from script import ceye_dns_api


class Engine():

    def __del__(self):

        logger.debug("Task over: %s" %self.name )

    def __init__(self,name):
        logger.sysinfo("Task created: %s",name)
        self.name = name
        self.queue = queue.Queue()
        self.targets = []
        self.modules = []
        self.parameter = None
        self.func_name = 'prove'
        self.put_queue_flag = True
        self.thread_count = self.thread_num  = conf['thread_num']
        self.scanning_count = self.scan_count = self.found_count = self.error_count = self.total = self.exclude =0
        self.is_continue = True
        self.queue_pool_total = 3000
        self.queue_pool_cache = 1000
        self.target_pool_total = 65535 * 255
        self.start_time =  self.current_time = time.time()
        self.set_thread_lock()

        logger.debug("引擎初始化!")

    def load_parameter(self):
        if 'parameter' in conf.keys() and conf['parameter'] != None:
            try:
                datas = conf['parameter'].split('&')
                dic = {}
                for _data in datas:
                    _key, _value = _data.split('=')
                    dic[_key] = _value
                self.parameter = dic
                logger.sysinfo("Loading parameter: %s" % (conf['parameter']))
            except:
                msg = 'The parameter input error, please check your input e.g. -p "userlist=user.txt", and you should make sure the module\'s function need the parameter. '
                sys.exit(logger.error(msg))

    def load_targets(self):

        if 'info' in conf.keys():
            if 'key' in conf.keys() and conf['key'] != None:
                _fofa()
            else:
                sys.exit(logger.error('请输入fofa语法!   -k XXX'))
        else:
            sys.exit(logger.error("Can't load any targets! Please check input." ))


    def set_thread_daemon(self,thread):
        thread.setDaemon(True)

    def put_target(self,obj,service = None):
        self.targets.append([obj, service])
        if len(self.targets) > self.target_pool_total:
            msg = 'Too many targets! Please control the target\'s numbers under the %d.' % self.target_pool_total
            sys.exit(logger.error(msg))

    def _put_queue(self):
        for module in self.modules:
            for i in range(0,len(self.targets)):
                obj, service = self.targets[i]
                if service !=None and service.lower() not in ['','unknown'] and service.lower() not in module.__name__.lower():
                    self.exclude += 1
                    continue

                self.queue.put([i+1,module,obj])
                if self.queue.qsize() >= self.queue_pool_total + self.queue_pool_cache:
                    yield self.queue
        yield self.queue


    def run(self):
        logger.sysinfo('任务 开始: %s', self.name)
        pool = self._put_queue()
        next(pool)

        self.print_progress()


        for i in range(0, self.thread_num):
            t = threading.Thread(target=self._work, name=str(i))
            self.set_thread_daemon(t)
            t.start()

        logger.debug("Wait for thread...")

        while True:
            if self.thread_count > 0 and self.is_continue:
                now_time = time.time()
                if now_time - self.current_time >= 60:
                    self.current_time = now_time
                    self.print_progress()

                if self.put_queue_flag and self.queue.qsize() < self.queue_pool_total:
                    try:
                        next(pool)
                        logger.debug("Add queue pool for engine.")
                    except StopIteration:
                        self.put_queue_flag = False

                time.sleep(0.01)

            else:
                self.print_progress()

                break

        logger.sysinfo('Task Finished: %s', self.name)

    def _work(self):
        while True:
            self.load_lock.acquire()
            if self.queue.qsize() > 0 and self.is_continue:
                id, module, target = self.queue.get(timeout=1.0)
                self.load_lock.release()
                self.change_scanning_count(+1)
                self._scan(id, module, target)
                self.change_scanning_count(-1)
                self.change_scan_count(1)
            else:
                self.load_lock.release()

                if not self.is_continue:
                    break

                # Wait for pool
                if self.total > self.queue_pool_total + self.queue_pool_cache:
                    time.sleep(3)

                if self.queue.qsize() <= 0 and self.scan_count == self.total:
                    break
                else:
                    continue

        self.change_thread_count(-1)

    def _scan(self, id, module, target):
        data = self._init_data(id, module, target)

        try:
            logger.debug("Test %s:%s for %s:%s" % (
                data['module_name'], self.func_name, data['target_host'], data['target_port']))
            func = getattr(module, self.func_name)

            module.logger = logger
            data = func(data)
            if conf.VERBOSE or data['flag'] == 1:
                if data['flag'] == 1:
                    self.found_count += 1


        except AttributeError:
            logger.error("Error %s:%s for %s:%s" % (
            data['module_name'], self.func_name, data['target_host'], data['target_port']))
            self.change_error_count(1)
        except KeyError as e:
            logger.error(
                "Missing necessary parameters: %s, please load parameters by -p. For example. -p cmd=whoami" % e)
        except Exception:
            self.errmsg = traceback.format_exc()
            self.is_continue = False
            logger.error(self.errmsg)

    def _init_data(self,id,module,target):
        data = {
            "id": id,
            "flag": -1,
            'module_name': module.__name__,
            'func_name': self.func_name,
            'target_host': None,
            'target_port': None,
            'url': None,
            'base_url': None,
            "data": [],
            "res": [],
            "other": {},
        }

        if self.parameter != None :
            for _key,_val in self.parameter.items():
                if _key not in data.keys():
                    data[_key] = _val
                else:
                    logger.warning("This parameter name has already been used: %s = %s" %( _key, _val))
                    logger.warning("And using this parameter name will cause the original value to be overwritten.")

        if target.startswith('http://') or target.startswith('https://'):
            data['url'] = target
            protocol, s1 = urllib.parse.splittype(target)
            host, s2 = urllib.parse.splithost(s1)
            host, port = urllib.parse.splitport(host)
            data['target_host'] = host
            data['target_port'] = port if port != None and port!= 0 else 443 if protocol == 'https' else 80
            data['base_url'] = protocol + "://" + host + ":" + str(data['target_port']) + '/'
        else:
            if ":" in target:
                _v = target.split(':')
                host, port = _v[0], _v[1]
                data['target_host'] = host
            else:
                port = 0
                data['target_host'] = target
            data['target_port'] = conf['target_port'] if 'target_port' in conf.keys() else int(port)

        return data


    def print_progress(self):
        self.total = len(self.targets) * len(self.modules) - self.exclude
        msg = '[%s] %s found | %s error | %s remaining | %s scanning | %s scanned in %.2f seconds.(total %s)' % (
            self.name, self.found_count, self.error_count, self.queue.qsize(),  self.scanning_count, self.scan_count, time.time() - self.start_time,self.total)
        logger.sysinfo(msg)

    def set_thread_lock(self):
        self.found_count_lock = threading.Lock()
        self.scan_count_lock = threading.Lock()
        self.thread_count_lock = threading.Lock()
        self.file_lock = threading.Lock()
        self.load_lock = threading.Lock()
        self.error_count_lock = threading.Lock()
        self.scanning_count_lock = threading.Lock()

    def change_thread_count(self,num):
        self.thread_count_lock.acquire()
        self.thread_count += num
        self.thread_count_lock.release()

    def change_scan_count(self,num):
        self.scan_count_lock.acquire()
        self.scan_count += num
        self.scan_count_lock.release()

    def change_scanning_count(self,num):
        self.scanning_count_lock.acquire()
        self.scanning_count += num
        self.scanning_count_lock.release()

    def change_error_count(self, num):
        self.error_count_lock.acquire()
        self.error_count += num
        self.error_count_lock.release()