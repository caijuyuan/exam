# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='\u4e3b\u952e', primary_key=True)),
                ('bk_biz_id', models.IntegerField(verbose_name='\u4e1a\u52a1ID')),
                ('bk_biz_name', models.CharField(max_length=128, verbose_name='\u4e1a\u52a1\u540d\u79f0')),
                ('bk_clound_id', models.IntegerField(verbose_name='\u4e91\u533a\u57dfid')),
                ('bk_clound_name', models.CharField(max_length=128, verbose_name='\u4e91\u533a\u57dfid')),
                ('os_name', models.CharField(max_length=128, verbose_name='\u7cfb\u7edf\u540d')),
                ('host_name', models.CharField(max_length=128, null=True, verbose_name='\u4e3b\u673a\u540d\u79f0')),
                ('ip', models.CharField(max_length=64, verbose_name='ip')),
                ('beizhu', models.CharField(max_length=64, null=True, verbose_name='\u5907\u6ce8')),
            ],
        ),
        migrations.CreateModel(
            name='Loadavg',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='\u4e3b\u952e', primary_key=True)),
                ('ip', models.CharField(max_length=64, verbose_name='ip')),
                ('bk_biz_id', models.IntegerField(verbose_name='\u4e1a\u52a1ID')),
                ('load_avg', models.FloatField(verbose_name='\u8d1f\u8f7d')),
                ('date', models.DateTimeField(null=True)),
            ],
        ),
    ]
