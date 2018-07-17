#from django.test import TestCase

# Create your tests here.

'''
print('{0}{1}'.format('q','e'))
merge_menu_dict 1 {'id': 1, 'caption': '菜单1', 'parent_id': None, 'child': [
    {'id': 4, 'caption': '菜单1.1', 'parent_id': 1, 'child': [
              {'id': 2, 'url': '/blog.html', 'caption': '博客管理', 'parent_id': 4, 'child': [], 'status': True},
              {'id': 6, 'caption': '菜单1.1.1', 'parent_id': 4, 'child': [], 'status': False}
                                                                   ], 'status': True},
    {'id': 5, 'caption': '菜单1.2', 'parent_id': 1, 'child': [
             {'id': 3, 'url': '/article.html', 'caption': '文章管理', 'parent_id': 5, 'child': [], 'status': True},
             {'id': 4, 'url': '/order.html', 'caption': '订单管理', 'parent_id': 5, 'child': [], 'status': True},
             {'id': 7, 'caption': '菜单1.2.1', 'parent_id': 5, 'child': [], 'status': False}
                                                                   ], 'status': True}
                                                                                ], 'status': True}
merge_menu_dict 2 {'id': 2, 'caption': '菜单2', 'parent_id': None, 'child': [
    {'id': 1, 'url': '/userinfo.html', 'caption': '用户管理', 'parent_id': 2, 'child': [], 'status': True}
                                                                                  ], 'status': True}
merge_menu_dict 3 {'id': 3, 'caption': '菜单3', 'parent_id': None, 'child': [], 'status': False}
merge_menu_dict 4 {'id': 4, 'caption': '菜单1.1', 'parent_id': 1, 'child': [
    {'id': 2, 'url': '/blog.html', 'caption': '博客管理', 'parent_id': 4, 'child': [], 'status': True},
    {'id': 6, 'caption': '菜单1.1.1', 'parent_id': 4, 'child': [], 'status': False}],
                   'status': True}
merge_menu_dict 5 {'id': 5, 'caption': '菜单1.2', 'parent_id': 1, 'child': [
    {'id': 3, 'url': '/article.html', 'caption': '文章管理', 'parent_id': 5, 'child': [], 'status': True},
    {'id': 4, 'url': '/order.html', 'caption': '订单管理', 'parent_id': 5, 'child': [], 'status': True},
    {'id': 7, 'caption': '菜单1.2.1', 'parent_id': 5, 'child': [], 'status': False}], 'status': True}
merge_menu_dict 6 {'id': 6, 'caption': '菜单1.1.1', 'parent_id': 4, 'child': [], 'status': False}
merge_menu_dict 7 {'id': 7, 'caption': '菜单1.2.1', 'parent_id': 5, 'child': [], 'status': False}
'''