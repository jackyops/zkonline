# coding:utf-8

__Author__ = 'eyu Fanne'
__Date__ = '2017/7/27'

from django.conf.urls import  url, include
from .views import MyMessageView



urlpatterns = [
    # 我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name="mymessage"),
    url(r'^mymessage/$', MyMessageView.as_view(), name="user_info"),
]