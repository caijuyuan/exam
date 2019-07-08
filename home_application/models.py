# -*- coding: utf-8 -*-
from django.db import models


class ExamModel(models.Model):
    id = models.AutoField(u'主键', primary_key=True)
    bk_biz_id = models.IntegerField(u'业务ID', null=True)
    bk_biz_name = models.CharField(u'业务ID', max_length=128, null=True)
    exam_name = models.CharField(u'模板', max_length=128, null=True)
    exam_type = models.CharField(u'ips', max_length=128, null=True)
    exam_addr = models.CharField(u'类型', max_length=128, null=True)
    exam_date = models.DateTimeField(u'开始', max_length=128, null=True)
    exam_charge = models.CharField(u'类型', max_length=128, null=True)
    exam_charge_phone = models.CharField(u'任务名称', max_length=128, null=True)
    exam_status = models.CharField(u'创建人', max_length=128, null=True)
    exam_topic = models.BinaryField(u'考试题目', null=True)
    exam_file_name = models.CharField(u'考试文件名', null=True, max_length=128)

    def __setitem__(self, key, value):
        self.key = value

    def __getitem__(self, item):
        return item

    def save_item(self, testobj):
        # 存储对象通用方法，处理外键或者when_created都需要先手动赋值对象或者原值后后再存储进去
        obj = self
        for attr in [f.name for f in self._meta.fields]:
            if (attr in testobj):
                setattr(obj, attr, testobj[attr])
        obj.save()

