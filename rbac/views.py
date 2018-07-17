from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import render
from . import models
# Create your views here.

def menu_filter_tree(res_list):
    ret = ''
    tpl = """
        <div>
            <div>%s</div>
            <div class='content'>%s</div>
        </div>
        """
    for row in res_list:
        if not row['status']:
            continue
        elif 'url' in row:
            ret += "<div><a href='%s' >%s</a></div>"%(row['url'],row['caption'])
        else:
            content = menu_filter_tree(row['child'])
            ret += tpl % (row['caption'], content)
    return ret

def menu_tree(res_list):
    ret=''
    tpl="""
    <div>
        <div>%s</div>
        <div class='content'>%s</div>
    </div>
    """
    for row in res_list:
        if not row['status']:
            continue
        content = menu_filter_tree(row['child'])
        ret += tpl %(row['caption'],content)
    return ret

def login(request):
    username = request.GET.get('u')
    user_obj = models.User.objects.get(username=username)
    #方式一
    #如果使用的是manytomany字段直接使用 m=manytomany('Role')
    #role_list = user_obj.m.all()可以获取到改用户对应的所有角色列表
    #方式2
    #直接使用User2Role表来查询查询结果为User2Role对象
    #models.User2Role.objects.filter(u=user_obj)
    #方式三直接使用role来查询
    #roleobj_list= models.Role.objects.filter(user2role__u=user_obj)
    #print(roleobj_list)
    #方式四
    roleobj_list = models.Role.objects.filter(user2role__u__username=username)
    #print(roleobj_list)

    #下一步根据角色获取所有权限(获取所有权限之后要么放在数据库里面要么放在session里面-推荐-权限修改之后需要重新登录重置session)
    #url_list = models.Permission2Action2Role.objects.filter(r__in=roleobj_list)
    url_list = models.Permission2Action.objects.filter(permission2action2role__r__in=roleobj_list).values('p__url','a__code').distinct()
    # for row in url_list:
    #     print(row)

    #获取URL(应该在菜单上显示的菜单，在最后一级)
    menu_url_list = models.Permission2Action.objects.filter\
        (permission2action2role__r__in=roleobj_list).exclude(p__menu__isnull=True).\
        values('p__id','p__url','p__caption','p__menu').distinct()
    menu_url_dict={}
    for row in menu_url_list:
        row = {
            'id':row['p__id'],
            'url':row['p__url'],
            'caption':row['p__caption'],
            'parent_id':row['p__menu'],
            'child':[],
            'status':True
        }
        if row['parent_id'] in menu_url_dict:
            menu_url_dict[row['parent_id']].append(row)
        else:
            menu_url_dict[row['parent_id']] = [row,]
    for i,j in menu_url_dict.items():
        print('menu_url_dict===>',i,j)


    #获取菜单列表
    menu_list = models.Menu.objects.all().values('id','caption','parent_id')
    menu_dict={}
    for row in menu_list:
        row['child'] = []
        menu_dict[row['id']] = row
    for k,v in menu_dict.items():
        v['status']=False
        print('menudict==>',k,v)
    for k,v in menu_url_dict.items():
        menu_dict[k]['child']=v
        parent_id = k
        while parent_id:
            menu_dict[parent_id]['status']=True
            parent_id = menu_dict[parent_id]['parent_id']
    for k,v in menu_dict.items():
        print('menu_dict_and_menu_url_dict==>',k,v)
    print('####处理等级关系')
    for k,v in menu_dict.items():
        if v['parent_id']:
            menu_dict[v['parent_id']]['child'].append(v)
        else:
            pass
    for k,v in menu_dict.items():
        print('merge_menu_dict',k,v)
    print('++++++++++++++++++++')
    result = []
    for row in menu_dict.values():
        if not row['parent_id']:
            result.append(row)
    # for k,v in menu_dict.items():
    #     print(k,v)
    # for row in result:
    #     print(row['caption'],row['status'])
    #     for r in row['child']:
    #         print('---->',r['caption'],row['status'])
    #         for n in r['child']:
    #             print('----------------->',n['caption'],n['status'])
    for i in result:
        print(i)

    str = menu_tree(result)
    return render(request,'rbac_index.html',{'str':str})