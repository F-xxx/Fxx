#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sdk import UcloudApiClient
from config import *
import sys
import json

#实例化 API 句柄

if __name__=='__main__':
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={
                "Action":"DescribeUHostInstance",
                "Region":"xx-xx",
                "UHostIds.n":" ",
               }
    response = ApiClient.get("/", Parameters);
    ret = json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))

    
    res = json.loads(ret)

    for item in res['UHostSet']:
        host = item["Name"]
        cpu = item["CPU"]
        memory = item["Memory"]
        state = item["State"]
        sys = item["BasicImageName"]
        local_ip = ""
        pub_ip = ""
        disk = ""
        for ip in item['IPSet']:
            if ip["Type"] == "Private":
                local_ip = ip['IP']
            if ip["Type"] == "International":
                pub_ip = ip['IP']

        for dis in item["DiskSet"]:
            if dis["Type"] == "Data":
                disk = dis['Size']

        print host,cpu,local_ip,pub_ip,disk,sys,state
