from .handler import Handler
from django.urls import re_path
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms


class BootStrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootStrapModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['readonly'] = 'readonly'


class Detail(Handler):
    name = 'detail'

    model_form_class = BootStrapModelForm

    def get_url(self):
        url = fr'{self.name}/(?P<pk>\d+)/$'
        return re_path(url, super().wrapper(self.detail), name=self.get_model_app_name(self.name))

    def detail(self, request, pk):

        """
        :param request:
        :param pk:
        :return:
        """
        current_change_object = self.model_class.objects.filter(pk=pk).first()
        if not current_change_object:
            return HttpResponse('The data to be modified does not exist, please select again!')

        model_form_class = self.get_modelform_class()
        if request.method == 'GET':
            form = model_form_class(instance=current_change_object)
            return render(request, 'crud/detail.html', {'form': form})
        return redirect(self.reverse_read_url())


