# -*- coding: utf-8 -*-
__author__ = 'Jacky'
__date__ = '2017/10/22 11:53'

import re
from django import forms
from operation.models import UserAsk

class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']

    """
    该方法必须以clean_字段名定义的函数，会主动去调用该函数
    验证手机号码是否合法
    """
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")

