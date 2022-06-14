from django.db import models
from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django.utils.module_loading import import_string

UserRbac = import_string(settings.USER_RBAC)


# Create your models here.

class Department(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=64, null=True)

    def __str__(self):
        return self.title


class User(UserRbac):
    """the table of User"""
    class Gender(models.TextChoices):
        SECRET = '0', _('Secret')
        MALE = '1', _('Male')
        FEMALE = '2', _('Female')

    gender = models.CharField(verbose_name=_('Gender'), max_length=8, choices=Gender.choices, default=0)

    level = models.SmallIntegerField(verbose_name=_('Level'), default=1)

    age = models.PositiveIntegerField(verbose_name=_('Age'), default=0)
    department = models.ForeignKey(verbose_name=_('Department'), to='Department', on_delete=models.CASCADE,
                                   related_name='departments', null=True, blank=True)

    def __str__(self):
        return self.username



