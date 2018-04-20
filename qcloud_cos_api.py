import sys
import qcloud_cos

appid=10000xxx
secret_id=u'xxxx'
secret_key=u'xxxx'
bucketname=u'bilogs'
region="guangzhou"

filein,fileout=sys.argv[1:]

cos_client = qcloud_cos.CosClient(appid, secret_id, secret_key, region)

def createCosDir(fileout):
    request = qcloud_cos.CreateFolderRequest(bucketname, fileout, u'bizAttribute')
    create_folder_ret = cos_client.create_folder(request)
    print "create folder result : ", create_folder_ret

def loadDataToCos(filein,fileout):
    request = qcloud_cos.UploadFileRequest(bucketname, fileout, filein, u'bizAttribute')
    upload_file_ret = cos_client.upload_file(request)
    print "upload file retresult : ", upload_file_ret

def getFileStat(filePath):
    request = qcloud_cos.StatFileRequest(bucketname, filePath)
    file_stat_ret = cos_client.stat_file(request)
    print "file stat retresult : ", file_stat_ret

if __name__ == '__main__':
    filein,fileout= sys.argv[1:]
    print "filein is ",unicode(filein)
    print "fileout is ",unicode(fileout)
    filein=unicode(filein)
    fileout=unicode(fileout)
    #createCosDir(fileout)
    loadDataToCos(filein,fileout)
    #getFileStat(fileout)



