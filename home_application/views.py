# -*- coding: utf-8 -*-
import StringIO
import time

import xlrd
import xlwt
from django.http import HttpResponse

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


# 解析excel
def get_execl(request):
    exam_id = request.POST.get('id')
    filename = '{0}.xls'.format(str(int(time.time())))
    file = open(filename, 'wb')
    file.write(request.FILES.get("exam_info").read())
    file.close()
    data = xlrd.open_workbook(filename)
    sheet = data.sheets()[0]
    nrows = sheet.nrows
    for i in range(nrows):
        if i == 0: continue
        values = sheet.row_values(i)
        inst_obj = ()
        inst_obj.exam_id = exam_id
        inst_obj.student_name = values[0]
        inst_obj.dopt = values[1]
        inst_obj.score = values[2]
        inst_obj.result = values[3]
        inst_obj.remark = values[4]
    return render_json(True)


# 导出excel
def export_excel(request):
    workbook = xlwt.Workbook()  # 注意Workbook的开头W要大写
    sheet = workbook.add_sheet('123', cell_overwrite_ok=True)
    row = 0
    sheet.write(row, 0, u'单位')
    sheet.write(row, 1, u'系统名')
    sheet.write(row, 2, u'time')
    sheet.write(row, 3, u'时长')
    sheet.write(row, 4, u'失败次数')
    # 保存该excel文件,有同名文件时直接覆盖
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=app_data.xls'
    output = StringIO.StringIO()
    workbook.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


# 导出文件
def download(request):
    id = request.GET.get('id')
    model_obj = ''
    response = HttpResponse(content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment;filename={0}'.format(model_obj)
    response.write(model_obj.read())
    return response