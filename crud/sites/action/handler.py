from abc import ABCMeta, abstractmethod
from django.urls import reverse
from crud.sites.components.bootstrap import BootstrapModelForm
import functools
from django.http import QueryDict


class Handler(object):
    handler_name = {'read': 'read',
                    'create': 'create',
                    'update': 'update',
                    'delete': 'delete',
                    'detail': 'detail'}

    def __init__(self, model_class, name_dict, prev):
        self._name = self.__class__.__name__.lower()
        self.model_class = model_class
        self.name_dict = name_dict
        self.prev = prev
        self.request = None
        self._modelform = None
        self.request = None
        self.model_form_class = None

    def get_url(self):
        raise NotImplementedError('You must implement this function!')

    def get_model_app_name(self, param):
        """
        app_model_param
        :param param:
        :return:
        """
        app_label = self.get_meta.app_label
        model_name = self.get_meta.model_name

        if self.prev:
            return f'{app_label}_{model_name}_{self.prev}_{param}'
        return f'{app_label}_{model_name}_{param}'

    @property
    def get_meta(self):
        return self.model_class._meta

    def get_reverse_name(self, param):
        namespace = self.name_dict.get('namespace')
        name = self.get_model_app_name(param)
        return f'{namespace}:{name}'

    def get_modelform_class(self):
        """
        customize you own ModelForm which contain clean_name function etc.
        :return:
        """
        if model_form_class := self.model_form_class:
            return model_form_class

        class DynamicModelForm(BootstrapModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"

        return DynamicModelForm

    def save_form(self, form, is_update=False):
        """
        Hook method reserved before saving data with ModelForm
        :param form:
        :param is_update:
        :return:
        """
        form.save()

    def wrapper(self, func):
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            self.request = request
            return func(request, *args, **kwargs)

        return inner

    def reverse_url(self, name,  *args, **kwargs):
        """
        When jumping back to the list page, generate the URL
        :return:
        """
        reverse_name = self.get_reverse_name(name)
        # update del create
        if name == 'update':
            base_url = reverse(reverse_name)
        base_url = reverse(reverse_name, args=args, kwargs=kwargs)

        if not self.request.GET:
            add_url = base_url
        else:
            param = self.request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict['_filter'] = param
            add_url = f'{base_url}?{param}'

        return add_url

    def reverse_read_url(self):
        """
        When jumping back to the list page, generate the URL
        :return:
        """
        reverse_name = self.get_reverse_name('read')
        base_url = reverse(reverse_name)
        param = self.request.GET.get('_filter')

        if not param:
            return base_url
        return f'{base_url}?{param}'
