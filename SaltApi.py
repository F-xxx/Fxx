# -*- coding:utf-8 -*-


#基于python3.x


import json
import ssl
from urllib import request, parse

class SaltApi(object):
    __token_id = ''
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    def __init__(self, url, username, password):
        self.__url = url.rstrip('/')
        self.__user = username
        self.__password = password

    def token_id(self):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        post_data_encode = parse.urlencode(params)  
        post_data_encode = post_data_encode.encode(encoding='utf-8')  
        content = self.postRequest(post_data_encode, prefix='/login')
        try:
            self.__token_id = content['return'][0]['token']
        except KeyError:
            raise KeyError

    def postRequest(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        req = request.Request(url, obj, headers=headers)
        response = request.urlopen(req)
        content = json.loads(response.read().decode('utf-8'))
        return content

    def list_all_key(self):
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        post_data_encode = parse.urlencode(params) 
        post_data_encode = post_data_encode.encode(encoding='utf-8')  
        self.token_id()
        content = self.postRequest(post_data_encode)
        minions = content['return'][0]['data']['return']['minions']
        print(minions)
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        return minions, minions_pre

    def salt_alive(self,tgt):
        params = {'client': 'local', 'tgt': tgt, 'fun': 'test.ping'}
        post_data_encode = parse.urlencode(params)  
        post_data_encode = post_data_encode.encode(encoding='utf-8')  
        self.token_id()
        content = self.postRequest(post_data_encode)
        ret = content['return'][0]
        return ret

    def delete_key(self,node_name):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        post_data_encode = parse.urlencode(params)  
        post_data_encode = post_data_encode.encode(encoding='utf-8')  
        self.token_id()
        content = self.postRequest(post_data_encode)
        ret = content['return'][0]['data']['success']
        print(ret)
        return ret

    def accept_key(self,node_name):
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
        post_data_encode = parse.urlencode(params)  
        post_data_encode = post_data_encode.encode(encoding='utf-8')  
        self.token_id()
        content = self.postRequest(post_data_encode)
        ret = content['return'][0]['data']['success']
        return ret

    def salt_runner(self,jid):
        params = {'client': 'runner', 'fun': 'jobs.lookup_jid', 'jid': jid}
        post_data_encode = parse.urlencode(params)  
        post_data_encode = post_data_encode.encode(encoding='utf-8') 
        self.token_id()
        content = self.postRequest(post_data_encode)
        ret = content['return'][0]
        return ret


    def salt_running_jobs(self):
        '''
        获取运行中的任务
        '''

        params = {'client':'runner', 'fun':'jobs.active'}
        post_data_encode = parse.urlencode(params)  
        post_data_encode = post_data_encode.encode(encoding='utf-8')
        self.token_id()
        content = self.postRequest(post_data_encode)
        ret = content['return'][0]
        return ret

    def remote_execution(self,tgt,fun,arg,expr_form):
        '''
        异步执行远程命令、部署模块
        '''

        params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        print(params)
        post_data_encode = parse.urlencode(params)  
        post_data_encode = post_data_encode.encode(encoding='utf-8')
        self.token_id()
        content = self.postRequest(post_data_encode)
        print(content)
        jid = content['return'][0]['jid']
        return jid

    def remote_localexec(self,tgt,fun,arg,expr_form):
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        post_data_encode = parse.urlencode(params) 
        post_data_encode = post_data_encode.encode(encoding='utf-8')
        self.token_id()
        content = self.postRequest(post_data_encode)
        ret = content['return'][0]
        return ret

    def salt_state(self,tgt,arg,expr_form):
        '''
        sls文件
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': expr_form}
        post_data_encode = parse.urlencode(params) 
        post_data_encode = post_data_encode.encode(encoding='utf-8') 
        self.token_id()
        content = self.postRequest(post_data_encode)
        ret = content['return'][0]
        return ret

def main():
    #sapi = SaltApi(url='',username='',password='')
    sapi = SaltApi(url='https://10.0.0.1:888', username='xxx', password='123')
    jid = sapi.remote_execution('localhost', 'cmd.run', 'df;echo ":::"$?', 'list')
    res = sapi.salt_alive('*')

if __name__ == '__main__':
    main()









