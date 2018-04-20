#!/usr/bin/python

import os
import sys
import qcloud_cos

appid=100002xxx
secret_id=u'xxx'
secret_key=u'xxx'
bucketname=u'backup'
region="guangzhou"

cos_client = qcloud_cos.CosClient(appid, secret_id, secret_key, region)

def upload_file(des,loc):
    request = qcloud_cos.UploadFileRequest(bucketname, des, loc, u'bizAttribute')
    upload_file_ret = cos_client.upload_file(request)
    print "upload file retresult : ", upload_file_ret

if __name__ == '__main__':
    loc,remote= sys.argv[1:]
    for path,dir,filelist in os.walk(loc):
        for filename in filelist:
            src = unicode(os.path.join(path,filename))
            des = unicode(src.replace(loc,remote))
            upload_file(des,src)





