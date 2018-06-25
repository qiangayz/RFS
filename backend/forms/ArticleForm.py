from django import forms as backend_forms
from django.forms import widgets as backend_widgets
from django.forms import fields as backend_fields
from django.core.exceptions import ValidationError
from repository import models



class ArticleForm(backend_forms.Form):
    title = backend_fields.CharField(
        error_messages={'required': '标题不能为空'},
        widget=backend_widgets.TextInput(attrs={'class':"form-control", 'id':"title"})
    )
    summary = backend_fields.CharField(
        error_messages={'required': '简介不能为空'},
        widget=backend_widgets.Textarea(attrs={'class':"form-control summary", 'id':"session"},
                                       )
    )
    content = backend_fields.CharField(
        error_messages={'required': '内容不能为空'},
        widget=backend_widgets.Textarea(attrs={'class':"form-control", 'id':"comment"})
    )
    article_type_id =backend_fields.IntegerField(
        error_messages={'required': '该项不能为空'},
        widget=backend_widgets.RadioSelect(choices=models.Article.type_choice)
    )
    category_id = backend_fields.ChoiceField(
        error_messages={'required': '该项不能为空'},
        choices = (),
        widget = backend_widgets.RadioSelect
    )
    tags = backend_fields.MultipleChoiceField(
        error_messages={'required': '该项不能为空'},
        choices = (),
        widget = backend_widgets.CheckboxSelectMultiple
    )
    def __init__(self,request,*args,**kwargs):
        super(ArticleForm,self).__init__(*args,**kwargs)
        blogid = request.session.get('blogid')
        self.fields['category_id'].choices = models.Category.objects.filter(blog_id=blogid).values_list('nid','title')
        self.fields['tags'].choices = models.Tag.objects.filter(blog_id=blogid).values_list('nid','title')