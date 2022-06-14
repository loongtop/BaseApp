from django.urls import re_path
from .views import user_create, user_list, department_list

app_name = 'web'

urlpatterns = [
    re_path(r'^user/list/$', user_list, name='user_list'),
    re_path(r'^user/create/$', user_create, name='user_create'),
    re_path(r'^department/list/$', department_list, name='department_create'),
]