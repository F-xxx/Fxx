#!/usr/bin/python

import time
import salt.client
import threadpool
from logger import *
from utils import color


class SaltApi(object):
    def __init__(self,arg,cmd):
        self.arg = arg
        self.cmd = cmd

    def salt(self,host):
        apis = salt.client.LocalClient()
        ret = apis.cmd(host, self.arg, [self.cmd])
        result = "{0}\n{1}".format(color.inYellow(host), ret[host])
#        print result
        logger.debug(result)

    def multi_task(self,file1):
        host_list = []
        with open(file1,'r') as f:
            host_list = [i.strip() for i in f]
            threadNum = len(host_list)
            print host_list
            pool = threadpool.ThreadPool(threadNum)
            requests = threadpool.makeRequests(self.salt, host_list)
            [pool.putRequest(req) for req in requests]
            pool.wait()


if __name__ == '__main__':
    pass

