from django.db import models
from django.utils.html import format_html

class UserInfo(models.Model):
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名',max_length=32,unique=True)
    nickname = models.CharField(verbose_name='昵称',max_length=32,null=True)
    password = models.CharField(verbose_name='密码',max_length=32)
    email = models.EmailField(verbose_name='邮箱',unique=True)
    avatar = models.ImageField(verbose_name='头像',null=True)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    fans = models.ManyToManyField(verbose_name='粉丝们',
                                  to='UserInfo',
                                  through='UserFans',
                                  related_name='f',
                                  through_fields=('user','follower'),
                                  )
    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '用户信息表'

class Blog(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题',max_length=64)
    site = models.CharField(verbose_name='个人博客前缀',max_length=32,unique=True)
    theme = models.CharField(verbose_name='博客主题',max_length=32)
    user = models.OneToOneField(to = 'UserInfo',to_field='nid',on_delete=models.CASCADE,related_name='blog')

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = '博客信息表'

class UserFans(models.Model):
    user = models.ForeignKey(verbose_name='博主',to='UserInfo',to_field='nid',related_name='users',on_delete=models.CASCADE)
    follower = models.ForeignKey(verbose_name='粉丝',to='UserInfo',to_field='nid',related_name='followers',on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('user','follower')
        ]
        verbose_name_plural = '粉丝表'

class Category(models.Model):
    """
    博主个人文章分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题',max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid',on_delete=models.CASCADE,related_name='category')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '用户自定义分类表'

class Article(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题',max_length=128)
    summary = models.TextField(verbose_name='文章简介',max_length=255)
    read_count = models.IntegerField(default=0,verbose_name='阅读量')
    ctime = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid',on_delete=models.CASCADE)
    category = models.ForeignKey(verbose_name='文章类型（自定义的）',to='Category',to_field='nid',null=True,on_delete=models.CASCADE)
    type_choice = [
        (1,'python'),
        (2,'linux'),
        (3,'java'),
        (4,'go'),
        (5,'openstack'),
    ]
    article_type_id = models.IntegerField(verbose_name='系统定义）',choices=type_choice,default=None)
    tags = models.ManyToManyField(to='Tag')

    def colored_status(self):
        return format_html(
            '<span style="color: #{};">{}</span>',
            'red',
            self.title,
        )
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章表'

class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称',max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid',on_delete=models.CASCADE,related_name='tag')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '标签表'

class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name='文章',to='Article',to_field='nid',on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签',to='Tag',to_field='nid',on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('article','tag'),
        ]
        verbose_name_plural = '标签文章对应表'

class ArticleDetail(models.Model):
    '''
    文章详细表
    '''
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(verbose_name='所属文章',to='Article',to_field='nid',on_delete=models.CASCADE,related_name='detail')

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name_plural = '文章详情表'

class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    content = models.TextField(verbose_name='评论内容',max_length=255)
    create_time = models.DateTimeField(verbose_name='评论时间',auto_now_add=True)
    reply = models.ForeignKey(verbose_name='回复评论',to='self',related_name='back',null=True,on_delete=models.CASCADE)
    acticle = models.ForeignKey(verbose_name='关联文章',to='Article',to_field='nid',on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='评论人',to='UserInfo',to_field='nid',on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = '评论表'

class UpDown(models.Model):
    """
    文章的顶或踩
    """
    acticle = models.ForeignKey(verbose_name='文章',to='Article',to_field='nid',on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='操作人',to='UserInfo',to_field='nid',on_delete=models.CASCADE)
    up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('acticle','user'),
        ]
        verbose_name_plural = '踩赞表'

class Trouble(models.Model):
    title = models.CharField(max_length=32,verbose_name='标题')
    detail= models.TextField(verbose_name='内容')
    user = models.ForeignKey(verbose_name='提交人',to=UserInfo,on_delete=models.CASCADE,related_name='u')
    # ctime = models.CharField(max_length=32)
    ctime = models.DateTimeField(verbose_name='创建时间')
    status_choices = (
        (1,'未处理'),
        (2,'处理中'),
        (3,'已处理')
    )
    status = models.IntegerField(choices=status_choices,default=1)
    processer = models.ForeignKey(verbose_name='处理者',to=UserInfo,on_delete=models.CASCADE,related_name='p',null=True,blank=True)
    solution = models.TextField(null=True)
    ptime = models.DateTimeField(null=True)
    pj_choices = (
        (1, '不满意'),
        (2, '一般'),
        (3, '很好')
    )
    pj = models.IntegerField(choices=pj_choices, default=1,null=True)

class Trouble_kill_demo(models.Model):
    title= models.CharField(max_length=32,verbose_name='标题')
    detail = models.TextField(verbose_name='内容')

