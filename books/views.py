from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.http import Http404

from .models import Book, Author, Category, process_books


class HomeView(ListView):
    template_name = "books_index.html"
    queryset = Category.objects.all()


class BookDetailsView(DetailView):
    template_name = "books_book_details.html"
    model = Book


class AuthorDetailsView(DetailView):
    template_name = "books_author_details.html"
    queryset = Author.objects.all()
    model = Author


class BookSearchMixin(object):
    paginate_by = 10

    def get_queryset(self):
        queryset = super(BookSearchMixin, self).get_queryset()
        q = self.request.GET.get('q', "").replace('"', "").replace("'", "")
        if q:
            q1 = queryset.filter(title__icontains=q)
            q2 = queryset.filter(description__icontains=q)
            final_q = q1 | q2
            return final_q.distinct()
        return queryset


class BookListView(BookSearchMixin, ListView):
    template_name = "books_book_list.html"
    model = Book


class CategoryListView(ListView):
    template_name = "books_category_list.html"
    model = Category


class CategoryDetailsView(BookSearchMixin, ListView, DetailView):
    template_name = "books_category_details.html"
    model = Category

    def get_object(self, queryset=None):
        return super(CategoryDetailsView, self).get_object(self.model._default_manager.all())

    def get(self, request, **kwargs):
        self.object = self.get_object()
        self.queryset = self.object.book_set.all()
        self.object_list = self.get_queryset()
        process_books(self.object_list, request.user)
        context = self.get_context_data(object=self.object, object_list=self.object_list)
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                        % {'class_name': self.__class__.__name__})
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super(CategoryDetailsView, self).get_context_data(**kwargs)
        context['category'] = self.object
        return context
        

class UserDetailsView(DetailView):
    template_name = "books_user_details.html"
    slug_field = "username"
    model = User
    context_object_name = "the_user"


