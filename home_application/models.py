# -*- coding: utf-8 -*-
from django.db import models


class Host(models.Model):
    id = models.AutoField(u'主键', primary_key=True)
    bk_biz_id = models.IntegerField(u'业务ID')
    bk_biz_name = models.CharField(u'业务名称', max_length=128)
    bk_clound_id = models.IntegerField(u'云区域id')
    bk_clound_name = models.CharField(u'云区域id', max_length=128)
    os_name = models.CharField(u'系统名', max_length=128)
    host_name = models.CharField(u'主机名称', max_length=128 ,null=True)
    ip = models.CharField(u'ip', max_length=64)
    beizhu = models.CharField(u'备注', max_length=64, null=True)


class Loadavg(models.Model):
    id = models.AutoField(u'主键', primary_key=True)
    ip = models.CharField(u'ip', max_length=64)
    bk_biz_id = models.IntegerField(u'业务ID')
    load_avg = models.FloatField(u'负载')
    date = models.DateTimeField(null=True)


class Load(models.Model):
    id = models.AutoField(u'主键', primary_key=True)
    ip = models.CharField(u'ip', max_length=64)
    bk_biz_id = models.IntegerField(u'业务ID')
    cpu_load = models.FloatField(u'cpu_load')
    memory_load = models.FloatField(u'memory_load')
    disk_load = models.FloatField(u'disk_load')
    date = models.DateTimeField(u'时间')