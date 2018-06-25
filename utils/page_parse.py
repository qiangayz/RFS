# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe

class Page(object):

    def __init__(self,curpage,all_count,page_tag=10,tagnum=7):
        self.curpage = int(curpage)
        self.all_count = int(all_count)
        self.page_tag = int(page_tag)
        self.tagnum = int(tagnum)

    @property
    def start(self):
        return (self.curpage - 1) * self.page_tag
    @property
    def end(self):
        return self.curpage * self.page_tag

    def page_str(self,url):
        count, y = divmod(self.all_count, self.page_tag)
        if y:
            count += 1
        page_list = []
        if count < self.tagnum:
            start_index = 1
            end_index = count + 1
        else:
            if self.curpage < (self.tagnum / 2) + 1:
                start_index = 1
                end_index = self.tagnum + 1
            else:
                start_index = self.curpage - ((self.tagnum - 1) / 2)
                end_index = self.curpage + ((self.tagnum - 1) / 2) + 1
                if (self.curpage + ((self.tagnum - 1) / 2) + 1) > count:
                    start_index = count - self.tagnum + 1
                    end_index = count + 1
        if self.curpage == 1:
            pre_str = '''<li><a aria-label = "Previous" href="javascript:void(0)">
            <span aria-hidden = "true"> 上一页 </span></a></li>'''
        else:
            pre_str = '''<li><a aria-label = "Previous" href="%s?p=%s&page_on_num=%s">
                        <span aria-hidden = "true"> 上一页 </span></a></li>''' % (url,
                self.curpage - 1, self.page_tag)
        page_list.append(pre_str)
        for i in range(int(start_index), int(end_index)):
            if i == self.curpage:
                pre_str = '<li class ="active"> <a href="%s?p=%s&page_on_num=%s"> %s </a> </li>' % (url, i, self.page_tag, i)
            else:
                pre_str = '<li> <a href="%s?p=%s&page_on_num=%s"> %s </a> </li>' % (url, i, self.page_tag, i)
            page_list.append(pre_str)
        if len(page_list) == 1:
            pre_str = '<li class ="active"> <a href="javascript:void(0)"> 1 </a> </li>'
            page_list.append(pre_str)
        if self.curpage == count:
            pre_str = '''<li><a aria-label = "Next" href="javascript:void(0)">
            <span aria-hidden = "true"> 下一页 </span></a></li>'''
        else:
            pre_str = '''<li><a aria-label = "Next" href="%s?p=%s&page_on_num=%s">
                        <span aria-hidden = "true"> 下一页 </span></a></li>'''% (url,
                self.curpage + 1, self.page_tag)
        page_list.append(pre_str)
        pake_str = ''.join(page_list)
        return mark_safe(pake_str)