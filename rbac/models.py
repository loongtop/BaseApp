from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Permission(models.Model):
    """
    the table of Permission
    """
    title = models.CharField(verbose_name=_('Title'), max_length=32)
    url = models.CharField(verbose_name=_('URL with RE'), max_length=128)

    # for the multi menu
    pid = models.ForeignKey(verbose_name=_('Permissions of super Menu'), to='Permission', null=True, blank=True,
                            related_name=_('parents'), on_delete=models.CASCADE)
    menu = models.ForeignKey(verbose_name=_('Belonging to the menu'), to='Menu', null=True, blank=True,
                             on_delete=models.CASCADE, help_text='Null means it is not a menu, '
                                                                 'non-null means it is a second class menu!')

    name = models.CharField(verbose_name=_('Alias of permission'), unique=True, max_length=32)

    def __str__(self):
        return self.title

    def get_all_pk_permission(self, pk):
        return self.objects.filter(id=pk).first()


class Role(models.Model):
    """
    the table of Role
    """
    title = models.CharField(verbose_name=_('Title'), max_length=32)
    permissions = models.ManyToManyField(verbose_name=_('Permission'), to='Permission', blank=True)

    def __str__(self):
        return self.title


class User(AbstractUser):
    """the table of User"""

    class Meta:
        """
        When doing database migration, this (abstract = True) can no longer create related
            tables and table structures for the User class.
        This class can be used as a "parent class" that is inherited by other Model classes.
        """
        abstract = True



class Menu(models.Model):
    """
    the Menu of Permission
    this is for multi-level menu which contains different permissions
    """
    title = models.CharField(verbose_name=_('First Class Menu Title'), max_length=32)
    icon = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.title
