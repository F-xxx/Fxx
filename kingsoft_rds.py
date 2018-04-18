#!/usr/bin/python
#coding:utf8

import re
import sys
import time
import base64
import datetime
import urllib
import uuid
import hashlib
import hmac
import urllib2
import optparse

AccessKeyId = 'Yxxx'
AccessKeySecret = '1xxxxxx'

primitive_params = {
    'Format' : 'xml',
    'Version' : '2015-05-31',
    'AccessKeyId' : AccessKeyId,
    'SignatureMethod' : 'HMAC-SHA256',
    'SignatureVersion' : '1',
    'SignatureNonce' : str(uuid.uuid1()),
    'Timestamp' : datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%dT%H:%M:%SZ')
}

parser = optparse.OptionParser()
parser.add_option("-i", 
		"--id", 
		help="The DbInstanceId on the Kingsoft Cloud "
		)
parser.add_option("-a", 
		"--action", 
		help="Perform the operation DescribeRdsBackup or CreateRdsBackup "
		)
parser.add_option("-r", 
		"--region", 
		help="region : cn-beijing-1 or other"
		)
parser.add_option("-n", 
		"--name", 
		help="back name"
		)

(options, args) = parser.parse_args()


def generate_url(params):
    sorted_params = sorted(params.items(), key=lambda x:x[0])

    encoded_params = map(lambda x:(urllib.quote(x[0]), urllib.quote(x[1])), sorted_params)

    canonical_query_string = '&'.join(map(lambda x: '%s=%s' % x, encoded_params))
    canonical_query_string = canonical_query_string.replace('/','%2F').replace('%7E','~')

    to_sign_string = 'GET' + '\n' + canonical_query_string

    h = hmac.new(AccessKeySecret, digestmod=hashlib.sha256)
    h.update(to_sign_string)

    signature = urllib.quote(base64.b64encode(h.digest()))

    url = 'https://api.ksyun.com/?%s&Signature=%s' % (canonical_query_string, signature)
    return url


#创建备份
def get_back_url(db_id, region,
		back_name='owner_%d' % int(time.strftime('%Y%m%d%H%M'))
		):
    aaa = primitive_params

    aaa['Action'] = 'CreateRdsBackup'
    aaa['Region'] = region
    aaa['BackupName'] = back_name
    aaa['DbInstanceId'] = db_id

    url = generate_url(aaa)
    return url


#查询RDS备份列表
def get_back_list_url(db_id, region):
    aaa = primitive_params

    aaa['Action'] = 'DescribeRdsBackup'
    aaa['Region'] = region
    aaa['DbInstanceId'] = db_id

    url = generate_url(aaa)
    return url

#输出备份执行结果
def output_back(arg):
    print arg
    aaa = '<BackupId>(.*?)</BackupId>'
    res = re.findall(aaa, arg)

    if res:
        print 'SUCCESS -----------> BackupId: ', res[0]
    else:
        print 'Failed------> '

#输出备份列表
def output_back_list(arg):

    aaa = '<BackupId>(.*?)</BackupId>.*?<BackupName>(.*?)</BackupName>.*?<CreationTime>(.*?)</CreationTime>'
    res = re.findall(aaa, arg)

    if not res:
        print '-------> NO DATA'
  
    for value in res:
        print value

def run_url(id, action, region, name):
    if action == 'back':
        if name:
            arg = "get_%s_url('%s', '%s', '%s')" % (action,id,region,name)

        else:
            arg = "get_%s_url('%s', '%s')" % (action,id,region)

    elif action == 'back_list':
        arg = "get_%s_url('%s', '%s')" % (action, id, region)

    result = eval(arg)


    try:
        response = urllib2.urlopen(result).read()
    except Exception, e:
        print 'Error--------------->', e
        sys.exit(-1)

    eval('output_%s(response)' % action)


if __name__ == '__main__':
    (options, args) = parser.parse_args()

    if not options.id or not options.action or not options.region:
        print parser.print_help()
        sys.exit(-1)

    run_url(options.id, options.action, options.region, options.name)


