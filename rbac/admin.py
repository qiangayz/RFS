from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Role)
admin.site.register(models.Action)
admin.site.register(models.Permission)
admin.site.register(models.Permission2Action)
admin.site.register(models.Permission2Action2Role)
admin.site.register(models.User)
admin.site.register(models.User2Role)
admin.site.register(models.Menu)
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = []
#
# @admin.register(Role)
# class RoleAdmin(admin.ModelAdmin):
#     list_display = []
#
# @admin.register(User2Role)
# class User2RoleAdmin(admin.ModelAdmin):
#     list_display = []
#
# @admin.register(Action)
# class ActionAdmin(admin.ModelAdmin):
#     list_display = []
#
# @admin.register(Permission)
# class PermissionAdmin(admin.ModelAdmin):
#     list_display = []
#
# @admin.register(Permission2Action)
# class Permission2ActionAdmin(admin.ModelAdmin):
#     list_display = []
#
# @admin.register(Permission2Action2Role)
# class Permission2Action2RoleAdmin(admin.ModelAdmin):
#     list_display = []