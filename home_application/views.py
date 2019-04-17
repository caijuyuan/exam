# -*- coding: utf-8 -*-
import json

import datetime
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from account.decorators import login_exempt
from common.mymako import render_mako_context
from  common.mymako import render_json
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
from home_application.esb_helper import cc_search_biz, cc_search_set, run_fast_execute_script, cc_search_host, \
    get_job_instance_log, get_host_ip_list, cc_get_job_detail, run_execute_job, cc_fast_push_file
from home_application.models import Host, Loadavg, Load


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/demo01_home.html')


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
    """
    测试
    """
    return render_mako_context(request, '/home_application/test.html')

def modal(request):
    """
    测试
    """
    return render_mako_context(request, '/home_application/modal.html')

def getJson(request):
    ip = request.GET.get('ip')
    data = list(Load.objects.filter(ip=ip).extra(
        select={'time': 'date', 'cpu': 'cpu_load', 'men': 'memory_load', 'disk': 'disk_load'}).
                values('time', 'cpu', 'men', 'disk'))
    # data = [
    #     {'time': '1月1日',  'cpu': 89.3, 'men': 96.4, 'disk':88},
    #     {'time': '1月2日',  'cpu': 79.3, 'men': 88.4, 'disk': 78},
    #     {'time': '1月3日',  'cpu': 88.3, 'men': 78.4, 'disk': 84},
    #     {'time': '1月4日', 'cpu': 78.3, 'men': 63.4, 'disk': 76},
    #     {'time': '1月5日',  'cpu': 74.3, 'men': 94.4, 'disk': 79},
    #     {'time': '1月6日',  'cpu': 85.3, 'men': 87.4, 'disk': 98}
    # ]
    return render_json({"result": True,"data": data})
# 返回echarts 图标拼接格式数据
# series 下面的type 表示需要渲染哪种图表类型
# line:折线图   bar:柱状图
def getEchartsJson(request):
    data ={
        "xAxis": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        "series": [
            {
                "name": "cpu",
                "type": "line",
                "data": [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
            },
            {
                "name": "men",
                "type": "line",
                "data": [3.6, 6.9, 8.0, 21.4, 23.7, 78.7, 165.6, 152.2, 68.7, 28.8, 7.0, 8.3]
            },
            {
                "name": "disk",
                "type": "bar",
                "data": [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
            }
        ]
    }
    return render_json({"result": True,"data": data})
# 该方法一般不作修改
def search_biz(request):
    data = cc_search_biz(request.user.username)
    return JsonResponse(data)


def search_set(request):
    """
    传递参数
    :param 业务id   biz_id
    :param request:
    :return:
    """
    biz_id = request.GET.get('biz_id')
    data = cc_search_set(biz_id)
    return JsonResponse(data)


def search_host(request):
    """
    :param request:
    传递参数
    :param 业务id   biz_id,
    biz_id,ip_list = ['10.92.190.214','10.92.190.215']
    get请求获取的ip_list，转换成列表，请调用get_host_ip_list
    :return:
    """
    biz_id = request.GET.get('biz_id')
    ip_list = []
    if 'ip' in request.GET:
        ip = request.GET.get('ip')
        ip_list = get_host_ip_list(ip)
    data = cc_search_host(biz_id,ip_list)
    return JsonResponse(data)


def fast_execute_script(request):
    """
    :param request:
    传递参数
    :param 业务id   biz_id,
         ip_list = [
            {
                "bk_cloud_id": 0,
                "ip": "10.92.190.214"
            }
            {
                "bk_cloud_id": 0,
                "ip": "10.92.190.215"
            }
        ]
    :return:
    """
    biz_id = request.GET.get('biz_id')
    script_content = """
         df -h
    """
    ip_list = [
        {
            "bk_cloud_id": 0,
            "ip": "192.168.240.43"
        }
    ]
    data = run_fast_execute_script(biz_id,script_content,ip_list,request.user.username)
    return JsonResponse(data)


def execute_job(request):
    """
    :param request:
    传递参数
    :param 业务id       biz_id,
    :param 作业模板id    job_id,
    :param ip列表     ip_list = [
            {
                "bk_cloud_id": 0,
                "ip": "10.92.190.214"
            }
            {
                "bk_cloud_id": 0,
                "ip": "10.92.190.215"
            }
        ]
    :return:
    """
    biz_id = request.GET.get('biz_id')
    job_id = request.GET.get('job_id')
    ip_list = [
        {
            "bk_cloud_id": 0,
            "ip": "192.168.240.43"
        }
    ]
    data = run_execute_job(biz_id, job_id, ip_list,request.user.username)
    return JsonResponse(data)


def get_log_content(request):
    """
        :param request:
        传递参数
        :param 业务id       biz_id,
        :param 作业实例id    instance_id,
        :return:
        """
    biz_id = request.GET.get('biz_id')
    job_instance_id = request.GET.get('instance_id')
    result = get_job_instance_log(biz_id, job_instance_id,request.user.username)
    data = {
        "data": result
    }
    return JsonResponse(data)


def job_detail(request):
    """
        :param request:
        传递参数
        :param 业务id       biz_id,
        :param 作业实例id    instance_id,
        :return:
        """
    biz_id = request.GET.get('biz_id')
    job_id = request.GET.get('job_id')
    data = cc_get_job_detail(biz_id, job_id, request.user.username)
    return JsonResponse(data)


def fast_push_file(request):
    biz_id = request.GET.get('biz_id')
    file_target_path = "/tmp/"
    target_ip_list = [{
      "bk_cloud_id": 0,
      "ip": "192.168.240.52"
    },
        {
      "bk_cloud_id": 0,
      "ip": "192.168.240.55"
    }
    ]
    file_source_ip_list = [{
            "bk_cloud_id": 0,
            "ip": "192.168.240.43"
        }
    ]
    file_source = ["/tmp/test12.txt","/tmp/test123.txt"]
    data = cc_fast_push_file(biz_id, file_target_path, file_source, target_ip_list, file_source_ip_list,request.user.username)
    return JsonResponse(data)


#  ============模拟考1================
def search_business1(request):
    result = cc_search_biz()
    return render_json(result)


def search_host1(request):
    bk_biz_id = request.GET.get('bk_biz_id')
    ips = request.GET.get('ips')
    ip_list = str(ips).split(',')
    result = cc_search_host(bk_biz_id, ip_list, request.user.username)
    for item in result['data']['info']:
        flag = Host.objects.filter(ip=item['host']['bk_host_innerip'], bk_biz_id=int(bk_biz_id)).exists()
        item['host']['is_moniter'] = True if flag else False
    return render_json(result)


def save_host1(request):
    try:
        bk_biz_id = request.GET.get('bk_biz_id')
        ip = request.GET.get('ip')
        result = cc_search_host(bk_biz_id, [ip])
        for info in result['data']['info']:
            item = info['host']
            host = Host.objects.filter(bk_biz_id=bk_biz_id, ip=item['bk_host_innerip'])
            if host:
                return render_json({'result': False, 'message': u'该主机已经添加'})
            host_obj = Host()
            host_obj.bk_biz_id = bk_biz_id
            host_obj.bk_biz_name = info['biz'][0]['bk_biz_name']
            host_obj.bk_clound_id = item['bk_cloud_id'][0]['bk_inst_id']
            host_obj.bk_clound_name = item['bk_cloud_id'][0]['bk_inst_name']
            host_obj.os_name = item['bk_os_name']
            host_obj.ip = item['bk_host_innerip']
            host_obj.host_name = item['bk_host_name']
            host_obj.save()
        return render_json({'result': True})
    except Exception, e:
        return render_json({'result': False, 'message': u'添加失败'})


def search_db_host1(request):
    ip = request.GET.get('ip')
    result = list(Host.objects.filter(ip__contains=ip).values())
    return render_json(result)

def delete_host1(request):
    bk_biz_id = request.GET.get('bk_biz_id')
    ip = request.GET.get('ip')
    Host.objects.filter(bk_biz_id=bk_biz_id, ip=ip).delete()
    return render_json({'result': True})


def execute(request):
    """
    查看性能
    """
    bk_biz_id = request.GET.get('bk_biz_id')
    ip = request.GET.get('ip')
    return render_mako_context(request, '/home_application/demo01_execute.html', {'bk_biz_id': bk_biz_id, 'ip': ip})


# ===== ============= 模拟考2 =============================
def test2(request):

    return render_json({'username': request.user.username, 'result': 'OK'})


def search_host_beizhu(request):
    bk_biz_id = request.GET.get('bk_biz_id')
    ip = request.GET.get('ip')
    host = Host.objects.filter(bk_biz_id=bk_biz_id, ip=ip).values()
    return render_json(list(host)[0])


def update_host_beizhu(request):
    bk_biz_id = request.GET.get('bk_biz_id')
    ip = request.GET.get('ip')
    beizhu = request.GET.get('beizhu')
    host = Host.objects.get(bk_biz_id=bk_biz_id, ip=ip)
    host.beizhu = beizhu
    host.save()
    return render_json({'result': True})


def get_chartData(request):
    data = {'type': u'已使用', 'value': 50}, {'type': u'剩余内存', 'value': 50}
    bk_biz_id = request.GET.get('bk_biz_id')
    ip = request.GET.get('ip')
    host = list(Host.objects.filter(bk_biz_id=bk_biz_id, ip=ip))
    if host:
        obj = host[0]
        r1 = run_execute_job(int(bk_biz_id), 2, [{"bk_cloud_id": obj.bk_clound_id, "ip": obj.ip}])
        if r1['result']:
            r2 = get_job_instance_log(int(bk_biz_id), r1['data'])
            for info in r2:
                if info['is_success']:
                    item = str(info['log_content'])
                    item = item.split('\n')
                    memory = item[1].split()
                    data = [{'type': u'已使用', 'value': memory[2]},{'type': u'剩余内存', 'value': memory[3]}]
    return render_json(data)



def get_tables(request):
    data = []
    bk_biz_id = request.GET.get('bk_biz_id')
    ip = request.GET.get('ip')
    host = list(Host.objects.filter(bk_biz_id=bk_biz_id, ip=ip))
    if host:
        obj = host[0]
        r1 = run_execute_job(int(bk_biz_id), 3, [{"bk_cloud_id": obj.bk_clound_id, "ip": obj.ip}])
        if r1['result']:
            r2 = get_job_instance_log(int(bk_biz_id), r1['data'])
            for info in r2:
                if info['is_success']:
                    item = str(info['log_content'])
                    item = item.split('\n')
                    for rows in item:
                        row = rows.split()
                        if row[0] == 'Filesystem':
                            continue
                        data.append({'name': row[0], 'total': row[1], 'yiyong_size': row[2], 'keyong_size': row[3], 'rate': row[4], 'dir': row[5]})
            return render_json(data)
        else:
            return render_json([{'name': 'name', 'total': 'total', 'yiyong_size': 'used', 'keyong_size': 'free', 'rate': 'rate', 'dir': 'dir'}])


def search_performan(request):
    bk_biz_id = request.GET.get('bk_biz_id')
    ip = request.GET.get('ip')
    bk_cloud_id = request.GET.get('bk_cloud_id')
    ip_list = [{
        "ip": ip,
        "bk_cloud_id": bk_cloud_id
    }]
    script_content = """
    MEMORY=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
    DISK=$(df -h | awk '$NF=="/"{printf "%s", $5}')
    CPU=$(top -bn1 | grep load | awk '{printf "%.2f%%", $(NF-2)}')
    DATE=$(date "+%Y-%m-%d %H:%M:%S")
    echo -e "$DATE|$MEMORY|$DISK|$CPU"
    """
    job_id = run_fast_execute_script(bk_biz_id, script_content, ip_list, request.user.username)
    if job_id['result']:
        result = get_job_instance_log(bk_biz_id, job_id['data'],request.user.username)
        logs = []
        for item in result:
            log_info = str(item['log_content'])
            info = log_info.replace("\n", '').split('|')
            if info.__len__() >= 4:
                log_info = {'date': info[0], 'memory_load': info[1], 'disk_load': info[2], 'cpu_load': info[3]}
                logs.append({'result': True, 'ip': item['ip'], 'log_info': log_info})
            else:
                logs.append({'result': False, 'ip': item['ip'], 'log_info': log_info})
        return render_json(logs)


# 添加监控
@csrf_exempt
@login_exempt
def insert_host(request):
    row = json.loads(request.body)
    if not row['row']['is_moniter']:
        bk_biz_id = int(row['bk_biz_id'])
        ip = row['row']['bk_host_innerip']
        result = cc_search_host(bk_biz_id, [ip])
        for info in result['data']['info']:
            item = info['host']
            host_obj = Host()
            host_obj.bk_biz_id = bk_biz_id
            host_obj.bk_biz_name = info['biz'][0]['bk_biz_name']
            host_obj.bk_clound_id = item['bk_cloud_id'][0]['bk_inst_id']
            host_obj.bk_clound_name = item['bk_cloud_id'][0]['bk_inst_name']
            host_obj.os_name = item['bk_os_name']
            host_obj.ip = item['bk_host_innerip']
            host_obj.host_name = item['bk_host_name']
            host_obj.save()
        obj = Host()
        obj.bk_biz_id = int(row['bk_biz_id'])
        obj.ip = row['row']['bk_host_innerip']
        obj.bk_clound_id = int(row['row']['bk_cloud_id'])
        return render_json({'result': True})
    else:
        Host.objects.filter(ip=row['row']['bk_host_innerip'],bk_biz_id=int(row['bk_biz_id'])).delete()
        return render_json({'result': False})



def get_ip_list(request):
    all_data = Host.objects.all().values('ip')

    return render_json(list(all_data))


def aa(request):
    all_data = Host.objects.all()
    now = datetime.datetime.now()
    biz_ips = {}
    for item in all_data:
        host = {
            "ip": item.ip,
            "bk_cloud_id": item.bk_clound_id
        }
        if str(item.bk_biz_id) in biz_ips:
            biz_ips[str(item.bk_biz_id)].append(host)
        else:
            biz_ips[str(item.bk_biz_id)] = [host]

    for biz in biz_ips:
        script_content = """
        MEMORY=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
        DISK=$(df -h | awk '$NF=="/"{printf "%s", $5}')
        CPU=$(top -bn1 | grep load | awk '{printf "%.2f%%", $(NF-2)}')
        DATE=$(date "+%Y-%m-%d %H:%M:%S")
        echo -e "$DATE|$MEMORY|$DISK|$CPU"
        """
        job_id = run_fast_execute_script(biz, script_content, biz_ips[biz])
        if job_id['result']:
            result = get_job_instance_log(biz, job_id['data'])
            logs = []
            for item in result:
                log_info = str(item['log_content'])
                info = log_info.replace("\n", '').split('|')
                if info.__len__() >= 4:
                    log_info = {'date': info[0], 'memory_load': info[1], 'disk_load': info[2], 'cpu_load': info[3]}
                    logs.append({'result': True, 'ip': item['ip'], 'log_info': log_info})
                else:
                    logs.append({'result': False, 'ip': item['ip'], 'log_info': log_info})
            for info in logs:
                if info['result']:
                    data = info['log_info']
                    host = Load()
                    host.bk_biz_id = int(biz)
                    host.ip = info['ip']
                    host.cpu_load = float(data['cpu_load'].replace("%", ''))
                    host.disk_load = float(data['disk_load'].replace("%", ''))
                    host.memory_load = float(data['memory_load'].replace("%", ''))
                    host.date = now
                    host.save()
