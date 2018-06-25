from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from repository.models import *

def index(request,*args,**kwargs):
    Article_type_id = None
    type_choice = Article.type_choice
    if kwargs:
        Article_type_id = int(kwargs['article_type_id'])
        Articlelist = Article.objects.filter(**kwargs).order_by('-nid')
    else:
        Articlelist = Article.objects.order_by('-nid')
    return render(request,'home.html',{'type_choice':type_choice,
                                       'Articlelist':Articlelist,
                                       'Article_type_id':Article_type_id,
                                       })

def test(request):
    if request.method == 'POST':
        print(request.POST.get('pwd'))
        fileobj=request.FILES.get('fafafafa')
        print(request.FILES)
        with open(fileobj.name, 'wb') as f:
            for item in fileobj.chunks():
                f.write(item)
    return  render(request,'home1.html')

def homesite(request,site):
    blogobj = Blog.objects.filter(site=site).select_related('user').first()
    article_list = Article.objects.filter(blog=blogobj).order_by('nid')
    request.session['blogid'] = blogobj.nid
    #date_list = Article.objects.raw(
    #    'select nid, count(nid) as num,date_format(ctime,"%Y-%m") as ctime from repository_article group by date_format(ctime,"%Y-%m");')
    date_list = Article.objects.raw(
        """select nid ,count(nid) as num, date_format(ctime,"%%Y-%%m") as create_time from repository_article  where blog_id=%s group by date_format(ctime,"%%Y-%%m");""",[blogobj.nid,])
    return render(request,'homesite.html',{'blogobj':blogobj,
                                           'article_list':article_list,
                                           'date_list': date_list})

def filter(request,blogsite,mode,modeid):
    blogobj = Blog.objects.filter(site=blogsite).select_related('user').first()
    article_list = Article.objects.filter(blog=blogobj).order_by('nid')
    date_list = Article.objects.raw(
        """select nid ,count(nid) as num, date_format(ctime,"%%Y-%%m") as create_time from repository_article  where blog_id=%s group by date_format(ctime,"%%Y-%%m");""",[blogobj.nid])
    if mode == 'tags':
        article_list = Article.objects.filter(blog__site=blogsite,tags__nid=modeid).order_by('nid')
    if mode == 'category':
        article_list = Article.objects.filter(blog__site=blogsite, category__nid=modeid).order_by('nid')
    if mode == 'date':
        article_list = Article.objects.filter(blog__site=blogsite).extra(where =['date_format(ctime,"%%Y-%%m")=%s'],params=[modeid,]).all().order_by('nid')
    return render(request, 'homesite.html', {'blogobj': blogobj,
                                                 'article_list': article_list,
                                                'date_list': date_list,
                                                 'mode':mode,
                                                 'modeid':modeid})

def detail(request,site,nid):
    blogobj = Blog.objects.filter(site=site).first()
    articleobj = Article.objects.filter(nid=nid).first()
    date_list = Article.objects.raw(
        """select nid ,count(nid) as num, date_format(ctime,"%%Y-%%m") as create_time from repository_article  where blog_id=%s group by date_format(ctime,"%%Y-%%m");""",
        [blogobj.nid])
    return render(request, 'articledetail.html', {'blogobj': blogobj,
                                             'articleobj': articleobj,
                                                  'date_list': date_list,
                                               })

def uploadimg(request):
    import json
    dic = {
        'error': 0,
        'url': '/static/img/4.jpg',
        'message': '错误了...'
    }

    return HttpResponse(json.dumps(dic))

