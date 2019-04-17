# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^test/$', 'test'),
    (r'^modal/$', 'modal'),
    (r'^api/getJson/$', 'getJson'),
    (r'^api/getEchartsJson/$', 'getEchartsJson'),

    (r'^search_biz/$', 'search_biz'),
    (r'^search_set/$', 'search_set'),
    (r'^search_host/$', 'search_host'),
    (r'^fast_execute_script/$', 'fast_execute_script'),
    (r'^execute_job/$', 'execute_job'),
    (r'^job_detail/$', 'job_detail'),
    (r'^get_log_content/$', 'get_log_content'),
    (r'^fast_push_file/$', 'fast_push_file'),

    # 模拟考1
    (r'^search_business1/$', 'search_business1'),
    (r'^search_host1/$', 'search_host1'),
    (r'^save_host1/$', 'save_host1'),
    (r'^search_db_host1/$', 'search_db_host1'),
    (r'^delete_host1/$', 'delete_host1'),
    (r'^execute/$', 'execute'),

    # 模拟考2
    (r'^api/test/$', 'test2'),
    (r'^search_host_beizhu/$', 'search_host_beizhu'),
    (r'^update_host_beizhu/$', 'update_host_beizhu'),
    (r'^api/get_chartData/$', 'get_chartData'),
    (r'^api/get_tables/$', 'get_tables'),

    # 模拟考3

(r'^search_performan/$', 'search_performan'),
(r'^insert_host/$', 'insert_host'),
(r'^get_ip_list/$', 'get_ip_list'),
(r'^aa/$', 'aa'),

)
