from django.urls import re_path
from django.shortcuts import render
from types import FunctionType
from django.db.models import Q

from .handler import Handler
from crud.utils.pagination import Pagination
from crud.sites.components.option import Option


class Read(Handler):
    name = 'read'
    per_page_count = 3

    display_list = []
    order_list = []
    action_list = []
    search_list = []
    search_value = []
    action_dict = {}
    search_group = []
    search_group_row_list = []

    has_create_btn = True

    def __init__(self, model_class, name_dict, prev):
        super().__init__(model_class, name_dict, prev)

        self.request = None
        self.name_dict = name_dict

    def read(self, request, *args, **kwargs):
        """
        :param request:
        :return:
        """
        # ########## 1. Action list ##########
        # 'multi_delete' or 'multi_init'
        name_list = self.get_action_list
        action_dict = {func.__name__: func.text for func in name_list}

        if request.method == 'POST':
            if action_func_name := request.POST.get('action'):
                if action_dict.get('action_func_name', None):
                    if action_response := getattr(self, action_func_name)(request, *args, **kwargs):
                        return action_response

        # ########## 2. search_list ##########
        search_list = self.get_search_list
        self.search_value = request.GET.get('q', '')

        conn = Q()
        conn.connector = 'OR'
        if self.search_value:
            for item in search_list:
                conn.children.append((item, self.search_value))

        # ########## 3. order_list ##########
        order_list = self.get_order_list
        search_group_condition = self.get_search_group_condition
        objects = self.model_class.objects.filter(conn).filter(**search_group_condition).order_by(*order_list)

        # ########## 4. Pagination ##########
        cnt = objects.count()
        params = request.GET.copy()
        params._mutable = True

        pager = Pagination(
            current_page=request.GET.get('page'),
            all_count=cnt,
            base_url=request.path_info,
            query_params=params,
            per_page=self.per_page_count,

        )

        # ########## 4. data_pack table ##########
        data_list = objects[pager.start: pager.end]

        # ########## 6. create btn #########

        # ########## 7.  combined search#########
        self.search_group_row_list = []
        for option_object in self.get_search_group:
            row = option_object.get_queryset_or_tuple(self.model_class, request, *args, **kwargs)
            self.search_group_row_list.append(row)

        data_pack = DataPack(self, data_list, pager)

        return render(request, 'crud/changelist.html', {'data_pack': data_pack})

    def get_url(self):
        return re_path(fr'{self.name}/$', super().wrapper(self.read), name=self.get_model_app_name(self.name))

    ########################################################################
    @property
    def get_create_btn(self):
        if self.has_create_btn:
            create_url = self.reverse_url('create')
            return f'<a class="btn btn-primary" href="{create_url}">Create</a>'
        return None

    @property
    def display(self):
        value = []
        value.extend(self.display_list)
        return value

    @property
    def get_action_list(self):
        return self.action_list

    @property
    def get_order_list(self):
        return self.order_list or ['-id', ]

    @property
    def get_search_list(self):
        return self.search_list

    @property
    def get_action_list(self):
        return self.action_list

    @property
    def get_search_group(self):
        return self.search_group

    @property
    def get_search_group_condition(self):
        """
        Get parameters for combinatorial search
        :param request:
        :return:
        """
        condition = {}
        # ?depart=1&gender=2&page=123&q=999
        for option in self.get_search_group:
            if option.is_multi:
                values_list = self.request.GET.getlist(option.field)  # tags=[1,2]
                if not values_list:
                    continue
                condition['%s__in' % option.field] = values_list
            else:
                value = self.request.GET.get(option.field)  # tags=[1,2]
                if not value:
                    continue
                condition[option.field] = value
        return condition


class DataPack(object):
    def __init__(self, config, data_list, pager):
        self.data_list = data_list
        self.display = config.display
        self.model_class = config.model_class
        self.pager = pager
        self.get_model_app_name = config.get_model_app_name
        self.request = config.request
        self.name_dict = config.name_dict
        self.search_list = config.search_list
        self.search_value = config.search_value
        self.action_dict = config.action_dict
        self.search_group_row_list = config.search_group_row_list
        self.create_btn = config.get_create_btn






