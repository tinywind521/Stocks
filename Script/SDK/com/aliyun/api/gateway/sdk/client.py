# -*- coding:utf-8 -*-
#  Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# coding=utf-8

import json
from com.aliyun.api.gateway.sdk.util import UUIDUtil, DateUtil
from com.aliyun.api.gateway.sdk.http.request import Request
from com.aliyun.api.gateway.sdk.http.response import Response
from com.aliyun.api.gateway.sdk.common import constant
from com.aliyun.api.gateway.sdk.auth import md5_tool, signature_composer, sha_hmac256


class DefaultClient:
    def __init__(self, appcode=None, time_out=None):
        self.__appcode = appcode
        self.__time_out = time_out
        pass

    def execute(self, request=None):
        try:
            headers = self.build_headers(request)

            response = Response(host=request.get_host(), url=request.get_url(), method=request.get_method(),
                                headers=headers, protocol=request.get_protocol(), content_type=request.get_content_type(),
                                content=request.get_body(), time_out=request.get_time_out())
            if response.get_ssl_enable():
                return response.get_https_response()
            else:
                return response.get_http_response()
        except IOError:
            raise
        except AttributeError:
            raise

    def build_headers(self, request=None):
        headers = dict()
        header_params = request.get_headers()
        headers[constant.X_CA_TIMESTAMP] = DateUtil.get_timestamp()
        headers[constant.Authorization] = "APPCODE "+ self.__appcode

        headers[constant.X_CA_NONCE] = UUIDUtil.get_uuid()

        if request.get_content_type():
            headers[constant.HTTP_HEADER_CONTENT_TYPE] = request.get_content_type()
        else:
            headers[constant.HTTP_HEADER_CONTENT_TYPE] = constant.CONTENT_TYPE_JSON

        headers[constant.HTTP_HEADER_ACCEPT] = constant.CONTENT_TYPE_JSON



        return headers
