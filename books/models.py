# -*- coding: utf-8 -*-
from django.db import models
# from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager


def process_books(books, user):
    if user.is_authenticated():
        for book in books:
            if user.get_profile().has_read_book(book):
                book.read = True
            elif user.get_profile().wants_book(book):
                book.is_wanted = True
            if user.get_profile().has_recommended_book(book):
                book.recommended = True
    return books


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    points = models.IntegerField(default=0, help_text="the current user points")
    bio = models.TextField(blank=True, null=True)
    books = models.ManyToManyField('Book', through='BookRelation')

    def wants_book(self, book):
        return self.books.filter(bookrelation__read=False, bookrelation__book=book).count() > 0

    def has_read_book(self, book):
        return self.books.filter(bookrelation__read=True, bookrelation__book=book).count() > 0

    def has_recommended_book(self, book):
        return self.user.recommendation_set.filter(book=book).count() > 0

    def _recommended_books(self):
        return Book.objects.filter(id__in=self.user.recommendation_set.all().values_list('book_id'))

    def recommended_books(self):
        return process_books(self._recommended_books(), self.user)

    def read_books(self):
        return process_books(self.books.filter(bookrelation__read=True), self.user)
        # .exclude(id__in=self._recommended_books()), self.user)

    def to_read_books(self):
        return process_books(self.books.filter(bookrelation__read=False), self.user)

    def __unicode__(self):
        return "User profile for %s" % self.user.username


class BookRelation(models.Model):
    user = models.ForeignKey('UserProfile')
    book = models.ForeignKey('Book')
    read = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s - %s" % (self.book, self.user.user.username)


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

    def get_absolute_url(self):
        return reverse('books_category_details', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
