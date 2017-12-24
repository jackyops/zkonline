workon zkonline


pip install Pillow
pip install MySQL-python

建议源码安装
pip install xadmin
添加app
    'xadmin',
    'crispy_forms',

同步xadmin的表
makemigrations
migrate

安装验证码
pip install django-simple-captcha
在INSTALLED_APPS添加
'captcha',
在URL添加
 url(r'^captcha/', include('captcha.urls')),

同步captcha的表
makemigrations
migrate