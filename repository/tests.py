#from django.test import TestCase

# Create your tests here.
type_choice = [
        (1,'python'),
        (2,'linux'),
        (3,'java'),
        (4,'go'),
        (5,'openstack'),
    ]
type_choice_list = map(lambda item:{'nid':item[0],'title':item[1]},type_choice)
for row in type_choice_list:
    print(row)