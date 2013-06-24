from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from .books.views import HomeView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='books_home'),
    # url(r'^about/$', HomeView.as_view(), name='about'),
)
