# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""
import json

import requests
from common.mymako import render_mako_context, render_json
from blueking.component.shortcuts import get_client_by_request
from conf.default import BK_APP_CODE, BK_APP_SECRET, BK_PAAS_HOST


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/index.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def test(request):
    client = get_client_by_request(request)
    kwargs = {}
    # result = client.cc.add_host_to_resource(kwargs)
    result = client.cc.get_user(kwargs)
    username = ''
    if result["result"]:
        username = result['data']['bk_username']
    return render_json({"result": True, "message": "success", "data": username})


def get_biz_list(request):
    """
    获取所有业务
    """
    biz_list = []
    client = get_client_by_request(request)
    kwargs = {
        'fields': ['bk_biz_id', 'bk_biz_name']
    }
    resp = client.cc.search_business(**kwargs)

    if resp.get('result'):
        data = resp.get('data', {}).get('info', {})
        for _d in data:
            biz_list.append({
                'name': _d.get('bk_biz_name'),
                'id': _d.get('bk_biz_id'),
            })

    result = {'result': resp.get('result'), 'data': biz_list}
    return render_json(result)


def get_host(request):
    """
    获取主机列表
    """
    host_list = []
    biz_id = int(request.POST.get('biz_id'))
    # ips = request.POST.get('ips')
    kwargs = {
        'bk_biz_id': biz_id,
    }
    client = get_client_by_request(request)
    result = client.search_host(**kwargs)
    if result.get('result'):
        data = result.get('data', {}).get('info', {})
        for _d in data:
            host_list.append({
                'host_ip': _d.get('host', {}).get('bk_host_innerip'),
                'os_name': _d.get('host', {}).get('bk_os_name'),
                'host_name': _d.get('host', {}).get('bk_host_name'),
                'name': _d.get('host', {}).get('bk_cloud_id'),
            })
    result = {'result': result.get('result'), 'data': host_list}
    return render_json(result)