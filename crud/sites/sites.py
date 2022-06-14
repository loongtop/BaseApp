from django.urls import re_path
from abc import ABCMeta, abstractmethod


class Site(metaclass=ABCMeta):
    """
    An Site object encapsulates an instance of the CRUD application, ready
    to be hooked in to your URLconf. Models are registered with the Site using the
    register() method, and the get_urls() method can then be used to access Django view
    functions that present a full admin interface for the collection of registered
    models.
    """

    @abstractmethod
    def register(self, model_class, handler_dict):
        pass

    @abstractmethod
    def get_urls(self):
        pass

    @abstractmethod
    def urls(self):
        pass


class CURDSite(Site):
    """
    Singleton
    """
    def __init__(self):
        self._registry = []
        self.namespace = ''
        self.app_name = ''

    def set_name(self, namespace, appname):
        self.namespace = namespace
        self.app_name = appname

    def register(self, *args, prev=None):
        """

        : param model_class: the class corresponding to the database table in the models
        : param handler_class: The class of the view function that handles the request
        : param prev: Generate URL prefix
        : return
        """
        self._registry = [{'model_class': item[0], 'handler_dict': item[1], 'prev': prev}
                          for model in args
                          for item in model]

    def get_urls(self):
        """
        : return urlpatterns
        """
        urlpatterns = []
        for model in self._registry:
            model_class = model['model_class']
            handler_dict = model['handler_dict']
            prev = model['prev']
            app_label = model_class._meta.app_label
            model_name = model_class._meta.model_name

            if prev:
                urlpatterns.append(re_path(fr'^{app_label}/{model_name}/{prev}',
                                           (self.create_urls(model_class, handler_dict, prev), None, None)))
            else:
                urlpatterns.append(
                    re_path(fr'^{app_label}/{model_name}/',
                            (self.create_urls(model_class, handler_dict, prev), None, None)))

        urlpatterns.extend(self.extra_urls())
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace

    def create_urls(self, model_class, handler_dict, prev):
        """
        : param model_class, handler_dict
        : return
        """
        urlpatterns = []
        name_dict = {'app_name': self.app_name, 'namespace': self.namespace}

        for operator_item in handler_dict.values():
            operator = operator_item(model_class, name_dict, prev)
            url = operator.get_url()
            urlpatterns.append(url)

        return urlpatterns

    def extra_urls(self):
        """
        you can add you own urls here
        : param
        : return
        """
        return []
