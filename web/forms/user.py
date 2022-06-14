from django.forms import ModelForm
from .help import BootstrapModelFormMixin
from ..models import User


class UserModelForm(BootstrapModelFormMixin, ModelForm):
    """
    the form of the customer
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'department', 'level', 'gender']
