#!/usr/bin/env python
#coding: utf8

import os
import time
from commands import getstatusoutput as getso

process_name = 'Battle'
soft_dir = '/data/fps/BattleServer'

def check_process():
    cmd = '''ps -ef | grep '%s' | grep -v grep ''' % process_name
    stat, res = getso(cmd)
    return res

def check_pid():
    os.chdir(soft_dir)
    res = os.path.getsize('service.pid')
    return res

def start_process():
    os.chdir(soft_dir)
    cmd = '''sh startup.sh'''
    os.system(cmd)
    os.system('''echo '%s ------> pull the process' >> /tmp/check.log ''' % cmd)


if __name__ == '__main__':
    pid = check_pid()
    if pid > 1:
        proc = check_process()
        if not proc:
            start_process()
            os.system('''echo '%s ------> pull the process' >> /tmp/check.log ''' % time.strftime('%Y-%m-%d %H:%M:%S')) 

