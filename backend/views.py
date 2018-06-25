from django.shortcuts import render
from django.shortcuts import redirect
from repository.models import *
from utils.page_parse import Page
from django.urls import reverse
from backend.forms import ArticleForm
from django.db import transaction
from utils.xss import XSSFilter
from django.utils.safestring import mark_safe

def index(request):
    return render(request,'backend/index.html')

def tag(request):
    pass

def category(request):
    pass

def base_info(request):
    pass


def article(request,**kwargs):
    condition = {}
    blogid = request.session.get('blogid')
    condition['blog_id'] = blogid
    blogobj = Blog.objects.filter(nid=blogid).select_related('user').first()
    type_choice_list = map(lambda item:{'nid':item[0],'title':item[1]},Article.type_choice)
    for i,j in kwargs.items():
        kwargs[i] = int(j)
        if j=='0'or i == 'typeseqid':
            pass
        else:
            condition[i]=j
    if kwargs['typeseqid'] == 0 :
        Articlelist = Article.objects.filter(**condition).order_by('-nid')
    else:
        Articlelist = Article.objects.filter(**condition).order_by('nid')
    curpage = request.GET.get('p',1)
    page_tag = request.GET.get('page_on_num',10)
    all_count = len(Articlelist)
    pageobj = Page(curpage,all_count,page_tag)
    Articlelist = Articlelist[pageobj.start:pageobj.end]
    # Articlelist = Article.objects.filter(tags__nid=3,blog_id=1).order_by('-nid')
    curURL = reverse('article',kwargs=kwargs)
    pake_str = pageobj.page_str(curURL)
    return render(request,'backend/article.html',{'Articlelist':Articlelist,
                                                  'blogobj':blogobj,
                                                  'type_choice_list':type_choice_list,
                                                  'argdict':kwargs,
                                                  'pake_str':pake_str ,})

def edit_article(request,nid):
    blogid = request.session.get('blogid')
    if request.method == 'GET':
        obj = Article.objects.filter(nid=nid,blog_id=blogid).first()
        if not obj:
            return render(request,'backend/no-article.html')
        tags = obj.tags.values_list('nid')
        if tags:
            tags=list(zip(*tags))[0]
        init_dict = {
            'nid':obj.nid,
            'title':obj.title,
            'summary':obj.summary,
            'category_id':obj.category_id,
            'article_type_id':obj.article_type_id,
            'content':obj.detail.content,
            'tags':tags
        }
        formobj = ArticleForm.ArticleForm(request=request,data=init_dict)
        return render(request,'backend/edit_article.html',{'form':formobj, 'nid':nid})
    elif request.method == "POST":
        form = ArticleForm.ArticleForm(request, data=request.POST)
        if form.is_valid():
            atricleobj = Article.objects.filter(nid=nid, blog_id=blogid).first()
            if not atricleobj:
                return render(request, 'backend/no-article.html')
            with transaction.atomic():
                tags = form.cleaned_data.pop('tags')
                content = form.cleaned_data.pop('content')
                content = XSSFilter().process(content)
                form.cleaned_data['blog_id'] = request.session.get('blogid')
                obj = Article.objects.filter(nid=atricleobj.nid).update(**form.cleaned_data)
                ArticleDetail.objects.filter(article=obj).update(content=content)
                atricleobj.tags.clear()
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(tag_id)
                atricleobj.tags.add(*tag_list)
            return redirect('/backend/article-0-0-0-0.html')
        else:
             return render(request, 'backend/edit_article.html', {'form': form,
                                                                 'nid': nid})


def add_article(request):
    if request.method == "GET":
        form  = ArticleForm.ArticleForm(request)
        return render(request,'backend/add_article.html',{'form':form,})
    elif request.method == "POST":
        form = ArticleForm.ArticleForm(request,data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                tags = form.cleaned_data.pop('tags')
                content = form.cleaned_data.pop('content')
                content = XSSFilter().process(content)
                form.cleaned_data['blog_id'] =  request.session.get('blogid')
                obj = Article.objects.create(**form.cleaned_data)
                ArticleDetail.objects.create(content=content,article=obj)
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(tag_id)
                obj.tags.add(*tag_list)
            return  redirect('/backend/article-0-0-0-0.html')

        else:
            return render(request,'backend/add_article.html',{'form':form,})
    else:
         return redirect('backend/article.html')

def del_article(requset,nid):
    Article.objects.filter(nid=nid).delete()
    return redirect('/backend/article-0-0-0-0.html')

def pagelist(requset):
    PAGRLIST = []
    for i in range(400):
        PAGRLIST.append(i)
    page_tag_list = [5, 10, 20, 50, 100]
    curpage = requset.GET.get('p',1)
    page_tag = requset.GET.get('page_on_num',10)
    all_count = len(PAGRLIST)
    pageobj = Page(curpage,all_count,page_tag)
    returndata = PAGRLIST[pageobj.start:pageobj.end]
    return render(requset, 'pagelist.html', {'dalist': returndata,
                                             'pake_str': pageobj.page_str('/backend/pagelist'),
                                             'page_tag_list': page_tag_list,
                                             'page_tag': page_tag})