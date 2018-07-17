from django import forms
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from repository.models import *
from web.forms import account
from utils.check_code import create_validate_code
from io import BytesIO
import json


def checkcodeimg(request):
    # f = open('test.png','wb')
    # img,code =  create_validate_code()
    # img.save(f)
    # f.close()
    f = BytesIO()
    img, code = create_validate_code()
    img.save(f, 'png')
    request.session['CheckCode'] = code
    return HttpResponse(f.getvalue())

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        check_obj = account.LoginForm(request.POST)
        if check_obj.is_valid():
            username = check_obj.cleaned_data.get('username')
            password = check_obj.cleaned_data.get('password')
            userinfo = UserInfo.objects.filter(username=username,password=password)
            reb =  check_obj.cleaned_data.get('rmb')
            checkcode = check_obj.cleaned_data.get('check_code')
            if checkcode.lower() == request.session['CheckCode'].lower():
                pass
            else:
                return render(request, 'login.html', {'check_res': '验证码错误'})
            if userinfo:
                request.session['userinfo'] = userinfo.first().nickname
                request.session['userinfo1'] = userinfo.first().nid

                try:
                    request.session['blogname'] = userinfo.first().blog.site
                except Exception:
                    request.session['blogname'] = None
                if reb:
                    request.session.set_expiry(60*60*24*7)
                return redirect('/')
            else:
                return render(request, 'login.html', {'check_res': '用户名或密码错误'})
        else:
            print(check_obj.errors.as_json())
        return render(request,'login.html',{'check_obj':check_obj})

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    if request.method == "POST":
        check_obj = account.Register(request.POST)
        if check_obj.is_valid():
            username = check_obj.cleaned_data.get('username')
            password = check_obj.cleaned_data.get('password')
            email = check_obj.cleaned_data.get('email')
            if UserInfo.objects.filter(username=username):
                return render(request, 'register.html', {'user_res_error': '用户已存在，请勿重复注册'})
            if UserInfo.objects.filter(email=email):
                return render(request, 'register.html', {'email_res_error': '邮箱已存在，请勿重复注册'})
            try:
                UserInfo.objects.create(username=username,password=password,email=email)
                return redirect('/login.html')
            except Exception as e:
                print(e)
                return render(request, 'register.html',{'res_error':'注册失败，原因未知'})
        else:
            return render(request, 'register.html',{'check_obj':check_obj})

def logout(request):
    request.session.clear()
    return redirect('/')

def check_code(request):
    pass