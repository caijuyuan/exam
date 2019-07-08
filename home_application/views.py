# -*- coding: utf-8 -*-
from blueking.component.shortcuts import get_client_by_request
from common.log import logger
from common.mymako import render_mako_context, render_json
from django.db.models import Q


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/dev/home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def search_business(request):
    try:
        client = get_client_by_request(request)
        kwargs = {"fields": [
            "bk_biz_id",
            "bk_biz_name"
        ],}
        result = client.cc.search_business(kwargs)
        return render_json(result)
    except Exception, e:
        print e
        logger.error(e)


def search_host(request):
    try:
        bk_biz_id = request.GET.get('bk_biz_id')
        if bk_biz_id:
            client = get_client_by_request(request)
            kwargs = {
                "bk_biz_id": int(bk_biz_id),
                "condition": [
                    {
                        "bk_obj_id": "host",
                        "fields": ["bk_host_innerip"],
                        "condition": []
                    }]
            }
            result = client.cc.search_host(kwargs)
            ip_list = []
            for item in result['data']['info']:
                ip_list.append(item['host'])
            return render_json(ip_list)
        else:
            return render_json()
    except Exception, e:
        print e
        logger.error(e)