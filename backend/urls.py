from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from backend import views

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
]