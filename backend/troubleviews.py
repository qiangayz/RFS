from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from repository.models import *
from django.forms import Form
from django.forms import widgets as backend_widgets
from django.forms import fields as backend_fields
from django.db.models import Q

"""
保障系统的需求：
普通用户：
    报障列表，创建报障，修改，【查看解决方案】【评分】
工程师：
    报障列表【自己已接单 or 未处理订单】
    列表：
         models.tb.objects.filter(Q(processor_id=1)|Q(status=1)).order_by('status')
    查看报障单id=1（抢单）：
         接单：v = models.tb.objects.filter(id=1,status=1).update(processor_id=22,status=2)
    处理：
         填写解决方案，提交status=3
                    ===》 模板
老板：
    查看所有信息
"""
def trouble_list(request,**kwargs):
    current_user_id = request.session.get('userinfo1')
    result = Trouble.objects.filter(user_id=current_user_id).order_by('status').\
        only('title','status','ctime','processer')
    if kwargs.get('typeid',None):
        result = Trouble.objects.filter(user_id=current_user_id).order_by('status'). \
            only('title', 'status', 'ctime', 'processer')
    else:
        result = Trouble.objects.filter(user_id=current_user_id).order_by('-status'). \
            only('title', 'status', 'ctime', 'processer')
    return render(request,'backend/backend_trouble_list.html',{'result':result,
                                                               'argdict':kwargs})


class trouble_createFrom(Form):
    title = backend_fields.CharField(
        widget=backend_widgets.TextInput(attrs={'class': 'form-control'})
    )
    detail = backend_fields.CharField(
        widget=backend_widgets.Textarea(attrs={'id':'detail'})
    )
import datetime
def trouble_create(request):
    current_user_id = request.session.get('userinfo1')
    if request.method == "GET":
        formobj = trouble_createFrom()
        return render(request,'backend/backend_trouble_create.html',{'formobj':formobj}
        )
    if request.method =="POST":
        form = trouble_createFrom(request.POST)
        if form.is_valid():
            dict1={}
            dict1['user_id'] = current_user_id
            dict1['ctime']  = datetime.datetime.now()
            dict1['status']  = 1
            dict1.update(form.cleaned_data)
            Trouble.objects.create(**dict1)
            return redirect('trouble-list.html')

def trouble_edit(request,nid):
    if request.method == "GET":
        obj1 = Trouble.objects.filter(id=nid,status=1).only('id','title','detail').first()
        if not obj1:
            return HttpResponse('当前状态不可操作')
        # form = trouble_createFrom({'title':obj1.title,'detail':obj1.detail})
        form = trouble_createFrom(initial={'title':obj1.title,'detail':obj1.detail})
        return render(request,'backend/backend_trouble_edit.html',{'formobj':form,
                                                                          'nid':nid})
    elif request.method == "POST":
        form = trouble_createFrom(data=request.POST)
        if form.is_valid():
            v = Trouble.objects.filter(id=nid,status=1).update(**form.cleaned_data)
            if not v:
                return HttpResponse('已被处理')
            else:
                return redirect('trouble-list.html')
        return render(request,'backend/backend_trouble_edit.html',{'formobj':form,
                                                                   'nid': nid})

def trouble_kill_list(request):
    current_user_id = request.session.get('userinfo1')
    if request.method == "GET":
        result = Trouble.objects.filter(Q(processer_id=current_user_id)|Q(status=1)).order_by('status')
        return  render(request,'backend/backend_trouble_kill_list.html',{
                                                                               'result': result,
                                                                                })

class trouble_kill_form(Form):
    solution = backend_fields.CharField(
        widget=backend_widgets.Textarea(attrs={'id':'solution','class':'kind-content'})
    )

def trouble_kill(request,nid):
    current_user_id = request.session.get('userinfo1')
    demo_list = Trouble_kill_demo.objects.all()
    if request.method == "GET":
        ret = Trouble.objects.filter(processer_id=current_user_id,id=nid).count()
        if not ret:
            v = Trouble.objects.filter(status=1,id=nid).update(status=2,processer_id=current_user_id)
            if not v:
                return HttpResponse('你手速太慢了，没抢到886')
        obj = Trouble.objects.filter(id=nid).first()
        formobj = trouble_kill_form(initial={'solution':obj.solution})
        demo_list = Trouble_kill_demo.objects.all()
        return render(request,'backend/backend_trouble_kil.html',{'form':formobj,
                                                                       'obj':obj,
                                                                  'demo':demo_list})
    if request.method == "POST":
        ret =  Trouble.objects.filter(id=nid,processer=current_user_id, status=2).count()
        if not ret:
            return HttpResponse('无法编辑')
        formobj = trouble_kill_form(request.POST)
        if formobj.is_valid():
            dic = {}
            dic['status'] = 3
            dic['solution'] = formobj.cleaned_data['solution']
            dic['ptime'] = datetime.datetime.now()
            Trouble.objects.filter(id=nid, processer=current_user_id, status=2).update(**dic)
            return redirect('/backend/trouble-kill-list.html')
        obj = Trouble.objects.filter(id=nid).first()
        return render(request, 'backend/backend_trouble_kil.html', {'obj': obj, 'form': formobj, 'nid': nid,
                                                                    'demo': demo_list})

def trouble_report(request):
    result = Trouble.objects.filter().order_by('-status'). \
        only('title', 'status', 'ctime', 'processer')
    return render(request,'backend/trouble_report.html',{
        "result":result
    })

def trouble_json_report(request):

    reponse = []
    from django.db import connection,connections
    userlist = UserInfo.objects.all()
    for row in userlist:
        cursor = connection.cursor()
        cursor.execute("""
        select unix_timestamp(date_format(ctime,"%%Y-%%m-01"))*1000 ,COUNT(id) from repository_trouble WHERE processer_id=%s GROUP BY date_format(ctime,"%%Y-%%m")
        """,[row.nid])
        result = cursor.fetchall()
        temp = {
            'name':row.username,
            'data':result
        }
        reponse.append(temp)
    import json
    return HttpResponse(json.dumps(reponse))

