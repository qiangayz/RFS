from django.forms import fields as ac_fields
from django import forms as ac_forms
from django.core.exceptions import ValidationError
from repository.models import *

class LoginForm(ac_forms.Form):
    username = ac_fields.CharField(error_messages={'required':'用户名不能为空'})
    password = ac_fields.CharField(error_messages={'required':'密码不能为空'})
    check_code = ac_fields.CharField(error_messages={'required':'验证码不能为空',                                            })
    # rmb = ac_fields.IntegerField(required=False)

class Register(ac_forms.Form):
    username = ac_fields.CharField(error_messages={'required': '用户名不能为空'})
    #password = ac_fields.CharField(error_messages={'required': '密码不能为空'})
    password = ac_fields.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=8,
        max_length=32,
        error_messages={'required': '密码不能为空.',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符"}
    )
    repassword = ac_fields.CharField(error_messages={'required': '确认密码不能为空'})
    email = ac_fields.CharField(error_messages={'required': '邮箱不能为空', 'invalid':'邮箱格式错误'})
    check_code = ac_fields.CharField(error_messages={'required': '验证码不能为空',
                                                     'invalid': '邮箱格式错误'})
    def clean(self):
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('repassword')
        if pwd1==pwd2:
            pass
        else:
            #from django.core.exceptions import ValidationError
            raise ValidationError('两次密码输入不一致')