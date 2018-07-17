from django.db import models

class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.username

class Role(models.Model):
    caption = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "角色表"

    def __str__(self):
        return self.caption

class User2Role(models.Model):
    u = models.ForeignKey(User,on_delete=models.CASCADE)
    r =models.ForeignKey(Role,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "用户分配角色"

    def __str__(self):
        return "{0}-{1}".format(self.u.username,self.r.caption)

class Action(models.Model):
    #每个url对应增删改查四个操作
    #增加：add
    #删除：delete
    #修改：put
    #获取：get
    caption = models.CharField(max_length=32)
    code = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "操作表"

    def __str__(self):
        return self.caption

class Menu(models.Model):
    caption = models.CharField(max_length=32)
    parent = models.ForeignKey('self',related_name='p',on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        verbose_name_plural = "菜单表"

    def __str__(self):
        return self.caption

class Permission(models.Model):
    caption = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    menu = models.ForeignKey(Menu,null=True,blank=True,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "url表"

    def __str__(self):
        return "{0}-{1}".format(self.caption,self.url)

class Permission2Action(models.Model):
    p = models.ForeignKey(Permission,on_delete=models.CASCADE)
    a = models.ForeignKey(Action,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "权限表"

    def __str__(self):
        return "{0}-{1}：-{2}?t={3}".format(self.p.caption,self.a.caption,self.p.url,self.a.code)

class Permission2Action2Role(models.Model):
    #用户权限有重复，查找到所有结果之后需要去重
    p2a = models.ForeignKey(Permission2Action,on_delete=models.CASCADE)
    r = models.ForeignKey(Role,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "角色分配权限"

    def __str__(self):
        return "{0}==》{1}".format(self.r.caption,self.p2a)

