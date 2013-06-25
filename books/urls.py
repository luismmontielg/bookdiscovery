from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.views.generic import TemplateView

from .views import HomeView, BookDetailsView, AuthorDetailsView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='books_home'),
    url(r'^book/(?P<slug>[-\w]+)/$', BookDetailsView.as_view(), name='books_book_details'),
    url(r'^author/(?P<pk>\d+)/$', AuthorDetailsView.as_view(), name='books_author_details'),
)
