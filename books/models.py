# -*- coding: utf-8 -*-
from django.db import models

from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_('user'))
    points = models.IntegerField(verbose_name=_("points"), default=0, help_text=_("the current user points"))
    bio = models.TextField(_('bio'), blank=True)
    # recommendations
    # books


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True 


class Recommendation(models.Model):
    book = models.ForeignKey('Book')
    review = models.TextField()
    tags = TaggableManager()
    # user 


class Book(BaseModel):
    title = models.CharField(max_length=100)
    author = models.ManyToManyField('Author')
    # categories
    # publisher
    # description
    # thumbnail url?

    def __unicode__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(verbose_name='Author', max_length=50)

    def __unicode__(self):
        return self.name


class Subject(BaseModel):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name
