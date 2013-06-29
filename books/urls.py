from django.conf.urls.defaults import patterns, url
from django.contrib import admin

from .views import HomeView, BookDetailsView, AuthorDetailsView, CategoryDetailsView, \
    BookListView, CategoryListView, UserDetailsView, RecommendationCreateView, \
    RecommendationDetailsView, RecommendationDeleteView, AddBookView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='books_index'),
    url(r'^books/$', BookListView.as_view(), name='books_book_list'),
    url(r'^users/(?P<slug>[-\w]+)/$', UserDetailsView.as_view(), name='books_user_details'),
    url(r'^book/(?P<id>\d+)/add_relation/$', AddBookView.as_view(), name='books_add_relation'),
    url(r'^book/(?P<slug>[-\w]+)/$', BookDetailsView.as_view(), name='books_book_details'),
    url(r'^book/(?P<slug>[-\w]+)/recommend/$', RecommendationCreateView.as_view(), name='books_recommendation_create'),
    url(r'^category/$', CategoryListView.as_view(), name='books_category_list'),
    url(r'^recommendations/(?P<pk>\d+)/$', RecommendationDetailsView.as_view(), name='books_recommendation_details'),
    url(r'^recommendations/(?P<pk>\d+)/delete/$', RecommendationDeleteView.as_view(), name='books_recommendation_delete'),
    url(r'^category/(?P<slug>[-\w]+)/$', CategoryDetailsView.as_view(), name='books_category_details'),
    url(r'^author/(?P<pk>\d+)/$', AuthorDetailsView.as_view(), name='books_author_details'),
)
