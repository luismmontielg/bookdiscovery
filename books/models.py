# -*- coding: utf-8 -*-
from django.db import models
# from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    points = models.IntegerField(default=0, help_text="the current user points")
    bio = models.TextField(blank=True, null=True)
    books = models.ManyToManyField('Book', through='BookRelation')

    def __unicode__(self):
        return "User profile for %s" % self.user.username


class BookRelation(models.Model):
    user = models.ForeignKey('UserProfile')
    book = models.ForeignKey('Book')
    read = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s - %s" % (self.book, self.user.username)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Recommendation(models.Model):
    book = models.ForeignKey('Book')
    user = models.ForeignKey(User)
    review = models.TextField()
    tags = TaggableManager()


class Book(BaseModel):
    authors = models.ManyToManyField('Author')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    categories = models.ManyToManyField('Category')
    publisher = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    thumbnail_url = models.URLField(blank=True, null=True, verify_exists=False)
    info_link = models.URLField(blank=True, null=True, verify_exists=False)
    tags = TaggableManager()

    @models.permalink
    def get_absolute_url(self):
        return reverse('books_book_details', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
