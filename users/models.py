# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _

# Create your models here.




class User(AbstractUser):
    email = models.EmailField(verbose_name=_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    def __unicode__(self):
        return self.get_full_name()


    def get_user_avatar(self):
        return self.userimage_set.last()




class UserImage(models.Model):
    class Meta:
        verbose_name = _('avatar')
        verbose_name_plural = _('avatars')

    user = models.ForeignKey(User, verbose_name=_('User'))
    avatar = models.ImageField(upload_to='users/avatars', verbose_name=_('Image'))

    def __unicode__(self):
        str(self.user) + ' -> ' + str(self.avatar)
