# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExamModel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='\u4e3b\u952e', primary_key=True)),
                ('bk_biz_id', models.IntegerField(null=True, verbose_name='\u4e1a\u52a1ID')),
                ('bk_biz_name', models.CharField(max_length=128, null=True, verbose_name='\u4e1a\u52a1ID')),
                ('exam_name', models.CharField(max_length=128, null=True, verbose_name='\u6a21\u677f')),
                ('exam_type', models.CharField(max_length=128, null=True, verbose_name='ips')),
                ('exam_addr', models.CharField(max_length=128, null=True, verbose_name='\u7c7b\u578b')),
                ('exam_date', models.DateTimeField(max_length=128, null=True, verbose_name='\u5f00\u59cb')),
                ('exam_charge', models.CharField(max_length=128, null=True, verbose_name='\u7c7b\u578b')),
                ('exam_charge_phone', models.CharField(max_length=128, null=True, verbose_name='\u4efb\u52a1\u540d\u79f0')),
                ('exam_status', models.CharField(max_length=128, null=True, verbose_name='\u521b\u5efa\u4eba')),
                ('exam_topic', models.BinaryField(verbose_name='\u8003\u8bd5\u9898\u76ee', null=True)),
                ('exam_file_name', models.CharField(max_length=128, null=True, verbose_name='\u8003\u8bd5\u6587\u4ef6\u540d')),
            ],
        ),
    ]
