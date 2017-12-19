# -*- coding: utf-8 -*-
__author__ = 'Jacky'
import  xadmin
from xadmin import views
from .models import EmailVerifyRecord,Banner


class BaseSetting(object):
    #启用主题
    enable_themes = True
    #添加多种主体
    use_bootswatch = True

class GlobalSetting(object):
    site_title = "教学管理平台"
    site_footer = "中控科技"
    #缩放菜单
    menu_style = "accordion"

class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']
class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)