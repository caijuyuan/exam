# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime
import json

import requests
from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from django.http import JsonResponse

from common.log import logger
from home_application.esb_helper import run_fast_execute_script, get_job_instance_log
from home_application.models import Host, Loadavg, Load


@task()
def async_task(x, y):
    """
    定义一个 celery 异步任务
    """
    logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    return x + y


def execute_task():
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
    # 调用定时任务
    async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    execute_task()
    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))


@task()
def insert_info():
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


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def insert_info_round():
    insert_info.delay()

    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))