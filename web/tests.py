import time
import random

def cal_time(func):          #该装饰器用来测量函数运行的时间
    def wrapper(*args,**kwargs):
        t1 = time.time()
        res = func(*args,**kwargs)
        t2 = time.time()
        print("%s running time: %s secs." % (func.__name__, t2 - t1))
        return res
    return wrapper

@cal_time
def line_search(data,val):
    # for i in range(len(data)):
    #     if data[i] == val:
    #         return i
    for i in data:
        if i == val:
            return data.index(i)
    return

@cal_time
def bin_search(data_set, val):
    #[1,2,3,4,5,6,7,8,9]  val = 3
    low = 0
    high = len(data_set) - 1
    while low <= high:
        mid = (low+high)//2
        if data_set[mid] == val:
            return mid
        elif data_set[mid] < val:
            low = mid + 1
        else:
            high = mid - 1
    return

# data = list(range(100000000))
# line_search(data,1733333)
# bin_search(data,1733333)

def random_create_dict(n):
    res = []
    nid_list = list(range(1000,1000+n))
    n1 = ['赵','钱','孙','李','周','吴','郑','王','慕容',]
    n2 = ['国','富','明','强','帅','军','飞','','']
    n3 = ['国', '富', '明', '强', '帅', '军', '飞', ]
    for i in range(n):
        arg = random.randint(16,60)
        nid=nid_list[i]
        name_list = random.choices(n1)+random.choices(n2)+random.choices(n3)
        name = ''.join(name_list)
        item = {'id':nid,'arg':arg,'name':name}
        res.append(item)
    return res

@cal_time
def bin_search_1(data_set, val):
    low = 0
    high = len(data_set) - 1
    while low <= high:
        mid = (low+high)//2
        if data_set[mid]['id'] == val:
            return mid
        elif data_set[mid]['id'] < val:
            low = mid + 1
        else:
            high = mid - 1
    return
data = random_create_dict(999999)
n = bin_search_1(data,88888)
print(n,data[n])