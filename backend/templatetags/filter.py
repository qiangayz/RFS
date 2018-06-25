from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def filter_all(argdict,typeid):
    TYPE_LIST = {'article_type_id':argdict['article_type_id'],
                 'category_id':argdict['category_id'],
                 'tags__nid':argdict['tags__nid'],
                 }
    for row in TYPE_LIST.keys():
        if row == typeid:
            TYPE_LIST[row] = 0
    TYPE_LIST = tuple(TYPE_LIST.values())
    if argdict[typeid] == 0:
        ret = '<li role="presentation" class="active"><a href="/backend/article-%s-%s-%s-0.html">全部</a></li>'%TYPE_LIST
    else:
        ret = '<li role="presentation" ><a href="/backend/article-%s-%s-%s-0.html">全部</a></li>'%TYPE_LIST
    return mark_safe(ret)

@register.simple_tag
def filterother(argdict,typeid,typelist):
    TYPE_DICT= {'article_type_id': argdict['article_type_id'],
                 'category_id': argdict['category_id'],
                 'tags__nid': argdict['tags__nid'],
                 }
    type_list=[]
    for row in typelist:
        try:
            type_id= row['nid']
        except Exception:
            type_id = row.nid

        for i in TYPE_DICT.keys():
            if i == typeid:
                    TYPE_DICT[i] = type_id
        list1 = list(TYPE_DICT.values())
        try:
             str1 = row['title']
        except Exception:
            str1 = row.title
        list1.append(str1)
        TYPE_LIST = tuple(list1)
        if argdict[typeid] == type_id:
            ret = '''<li role="presentation" class="item active" >
            <a href="/backend/article-%s-%s-%s-0.html">
            %s</a></li>'''%TYPE_LIST
        else:
            ret = '''<li role="presentation" class="item" >
                        <a href="/backend/article-%s-%s-%s-0.html">
                        %s</a></li>''' % TYPE_LIST
        type_list.append(ret)
    type_str = ''.join(type_list)
    return mark_safe(type_str)
