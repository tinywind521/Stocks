# -*- coding: utf-8 -*-
from com.aliyun.api.gateway.sdk import client
from com.aliyun.api.gateway.sdk.http import request
from com.aliyun.api.gateway.sdk.common import constant
import json


class ShowapiRequest:
    def __init__(self,url,appcode):
        self.__time_out=30000
        self.__url = url
        self.__appcode = appcode
        self.__body = {}
        print (appcode)
        ind=url.index("/",8)
        self.__host = url[0:ind]
        self.__url = url[ind:]
        print (ind)
        print (self.__host)
        print (self.__url)


    def addTextPara(self,k,v):
        self.__body[k]=v
        return self

    def get(self):
        self.__url=self.__url+'?'
        for k,v in self.__body.items():
            self.__url=self.__url+k+"="+str(v)+"&"
        self.__url=self.__url[0:len(self.__url)-1]
        print ("send data")
        cli = client.DefaultClient( self.__appcode )
        req = request.Request(host= self.__host,protocol=constant.HTTP, url=self.__url, method="GET", time_out=self.__time_out)
        res= cli.execute(req)
        json_res=json.dumps(res[2])
        return json_res

    def post(self):
        print ("send data")
        cli = client.DefaultClient( self.__appcode)
        req = request.Request(host= self.__host,protocol=constant.HTTP, url=self.__url, method="POST", time_out=self.__time_out)
        req.set_body(self.__body)
        # for k,v in self.__body.items():
        #     print "key:"+k+",value:"+str(v)
        req.set_content_type(constant.CONTENT_TYPE_FORM)
        res= cli.execute(req)
        json_res=json.dumps(res[2])
        return json_res

    def set_time_out(self, time_out):
        self.__time_out = time_out
        return self

