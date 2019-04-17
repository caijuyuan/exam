# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Load',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='\u4e3b\u952e', primary_key=True)),
                ('ip', models.CharField(max_length=64, verbose_name='ip')),
                ('bk_biz_id', models.IntegerField(verbose_name='\u4e1a\u52a1ID')),
                ('cpu_load', models.FloatField(verbose_name='cpu_load')),
                ('memory_load', models.FloatField(verbose_name='memory_load')),
                ('disk_load', models.FloatField(verbose_name='disk_load')),
                ('date', models.DateTimeField(verbose_name='\u65f6\u95f4')),
            ],
        ),
    ]
