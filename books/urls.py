from django.conf.urls.defaults import patterns, url
from django.contrib import admin

from .views import HomeView, BookDetailsView, AuthorDetailsView, CategoryDetailsView, BookListView, CategoryListView, UserDetailsView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='books_index'),
    url(r'^books/$', BookListView.as_view(), name='books_book_list'),
    url(r'^users/(?P<slug>[-\w]+)/$', UserDetailsView.as_view(), name='books_user_details'),
    url(r'^book/(?P<slug>[-\w]+)/$', BookDetailsView.as_view(), name='books_book_details'),
    url(r'^category/$', CategoryListView.as_view(), name='books_category_list'),
    url(r'^category/(?P<slug>[-\w]+)/$', CategoryDetailsView.as_view(), name='books_category_details'),
    url(r'^author/(?P<pk>\d+)/$', AuthorDetailsView.as_view(), name='books_author_details'),
)
