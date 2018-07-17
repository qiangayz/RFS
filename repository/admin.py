from django.contrib import admin
from repository.models import *

# Register your models here.


# class UserInfoAdmin(admin.ModelAdmin):
#     list_display = ('nid', 'username', 'nickname', 'password', 'email', 'create_time')
#
#
# admin.site.register(UserInfo, UserInfoAdmin)

admin.site.site_header = '后台管理'
admin.site.site_title = '后台管理'

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('nid', 'username', 'nickname', 'password', 'email', 'create_time')

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 3

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-nid',)

    # list_editable 设置默认可编辑字段
    list_editable = ['email', 'nickname']

    # fk_fields 设置显示外键字段
    fk_fields = ('fans_id',)

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('password', 'create_time')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['nid','title','blog']
    list_editable = ['title', 'blog']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    def show_tags(self,obj):
        return [row.title for row in obj.tags.all()]
    filter_horizontal = ('tags',)

    list_display = ['nid','show_tags','title','summary','read_count','ctime','blog','category','article_type_id']
    list_filter = ('title',)  # 过滤器
    search_fields = ('title', )  # 搜索字段
    date_hierarchy = 'ctime'  # 详细时间分层筛选　
    ordering = ('nid',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','site','theme','user']
    list_editable = ['site','theme','user']

@admin.register(UserFans)
class UserFansAdmin(admin.ModelAdmin):
    list_display = ['user','follower']
    list_editable = ['follower']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title','blog']
    list_editable = ['blog']

@admin.register(ArticleDetail)
class ArticleDetailAdmin(admin.ModelAdmin):
    list_display = ['id','article',]
    ordering = ('id',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'reply', 'acticle', 'user']

@admin.register(UpDown)
class UpDownAdmin(admin.ModelAdmin):
    list_display = ['acticle','user','up']


@admin.register(Trouble_kill_demo)
class Trouble_kill_demoAdmin(admin.ModelAdmin):
    list_display = ['title','detail',]

@admin.register(Trouble)
class TroubleAdmin(admin.ModelAdmin):

    list_display = ['title','user','ctime','status','processer']
    # list_editable 设置默认可编辑字段
    list_editable = ['processer', 'ctime','status']
