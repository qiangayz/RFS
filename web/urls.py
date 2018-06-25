from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls import url
from web.views import home
from web.views import account

urlpatterns = [
    path(r'',home.index),
    path(r'test',home.test),
    path(r'login.html',account.login),
    path(r'register.html',account.register),
    path(r'logout.html',account.logout),
    path(r'check_code.html',account.check_code),
    path(r'checkcodeimg',account.checkcodeimg),
    # url(r'sel-(.+).html',home.index),
    # url(r'sel-(?P<article_type_id>\d+).html',home.index),
    url(r'sel-(?P<article_type_id>\d+).html',home.index,name='index'),
    url(r'^(?P<blogsite>\w+)/(?P<mode>((tags)|(category)|(date)))/(?P<modeid>\w+-*\w*).html',home.filter),
    url(r'^(?P<site>\w+).html$',home.homesite),
    url(r'^(?P<site>\w+)/(?P<nid>\d+).html$',home.detail),
    url(r'^uploadimg',home.uploadimg),

]