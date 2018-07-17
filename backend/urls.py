from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from backend import views
from . import troubleviews

urlpatterns = [
    path('index.html',views.index ),
    url(r'^tag.html$', views.tag),
    url(r'^category.html$', views.category),
    url(r'^base-info.html$', views.base_info),
    url(r'^pagelist$', views.pagelist),
    url(r'^article-(?P<article_type_id>\d+)-(?P<category_id>\d+)-(?P<tags__nid>\d+)-(?P<typeseqid>((0)|(1))*).html$', views.article,name='article'),
    url(r'^add-article.html$', views.add_article),
    url(r'^edit-article-(?P<nid>\d+).html$', views.edit_article),
    url(r'^del-article-(?P<nid>\d+).html$', views.del_article),
# 一般用户： 提交报障单,查看，修改（未处理），评分（处理完成，未评分）
    url(r'^trouble-list.html(?P<typeid>\d*)$', troubleviews.trouble_list),
    url(r'^trouble-create.html$', troubleviews.trouble_create),
    url(r'^trouble-edit-(\d+).html$', troubleviews.trouble_edit),
    url(r'^trouble-kill-list.html$', troubleviews.trouble_kill_list),
    url(r'^trouble-report.html$', troubleviews.trouble_report),
    url(r'^trouble-json-report.html$', troubleviews.trouble_json_report),
]