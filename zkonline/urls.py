"""zkonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
# django处理静态文件内容
from django.views.static import serve
from zkonline.settings import MEDIA_ROOT

import xadmin

from users.views import LoginViews,RegisterViews,ActiveUserView,ForgetPwdViews,RestView,ModifyPwdView


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'login/$', LoginViews.as_view(), name="login"),
    url(r'register/$', RegisterViews.as_view(), name="register"),
    url(r'forget_pwd/$', ForgetPwdViews.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<reset_code>.*)/$', RestView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="logout"),

    # media的url配置，图片上传的url路径
    url(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    #课程相关url配置
    url(r'^course/', include('courses.urls', namespace="course")),

    # 用户
    url(r'^users/', include('users.urls', namespace="users")),


    #课程机构首页
    url(r'^org/', include('organization.urls', namespace="org")),

]
