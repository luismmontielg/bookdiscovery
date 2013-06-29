from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, View
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.http import Http404, HttpResponseRedirect
from django.db.models import Count
from django.contrib import messages
from django.shortcuts import get_object_or_404

from braces.views import JSONResponseMixin, AjaxResponseMixin, LoginRequiredMixin

from .models import Book, Author, Category, process_books, UserProfile, Recommendation
from .forms import UserProfileForm, RecommendationForm


class HomeView(ListView):
    template_name = "books_index.html"
    queryset = Category.objects.all()


class BookDetailsView(DetailView):
    template_name = "books_book_details.html"
    context_object_name = "book"
    model = Book

    def get_object(self, queryset=None):
        book = super(BookDetailsView, self).get_object(queryset)
        return process_books([book], self.request.user)[0]

    def get_context_data(self, **kwargs):
        context = super(BookDetailsView, self).get_context_data(**kwargs)
        context["recommendation_form"] = RecommendationForm(initial={"user": self.request.user,\
                "book": self.object})
        context["can_recommend"] = self.request.user.get_profile().can_recommend_book(self.object)

        if self.request.user.is_authenticated():
            context["the_user"] = self.request.user.get_profile()
        return context

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
    queryset = Book.ordered.all()

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context["the_user"] = self.request.user.get_profile()
        return context

    def paginate_queryset(self, queryset, page_size):
        (paginator, page, objects, other_pages) = super(BookListView, self).paginate_queryset(queryset, page_size)
        return (paginator, page, process_books(objects, self.request.user), other_pages)


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
        self.queryset = self.object.book_set.all().annotate(Count("recommendation")).order_by("-recommendation", "title")
        self.object_list = self.get_queryset()
        # process_books(self.object_list, request.user)
        context = self.get_context_data(object=self.object, object_list=self.object_list)
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                        % {'class_name': self.__class__.__name__})
        context = self.get_context_data(object_list=self.object_list)
        if self.request.user.is_authenticated():
            context["the_user"] = self.request.user.get_profile()
        return self.render_to_response(context)

    def paginate_queryset(self, queryset, page_size):
        (paginator, page, objects, other_pages) = super(CategoryDetailsView , self).paginate_queryset(queryset, page_size)
        return (paginator, page, process_books(objects, self.request.user), other_pages)


    def get_context_data(self, **kwargs):
        context = super(CategoryDetailsView, self).get_context_data(**kwargs)
        context['category'] = self.object
        return context


class UserDetailsView(UpdateView):
    template_name = "books_user_details.html"
    slug_field = "user__username"
    model = UserProfile
    context_object_name = "the_user"
    form_class = UserProfileForm

    def form_valid(self, form):
        msg = "Profile was updated!"
        messages.info(self.request, msg)
        return super(UserDetailsView, self).form_valid(form)


class AjaxRecommendationDeleteView(JSONResponseMixin, AjaxResponseMixin, CreateView):
    model = Recommendation


class RecommendationCreateView(LoginRequiredMixin, CreateView):
    model = Recommendation
    template_name = "books_recommendation_create.html"
    form_class = RecommendationForm

    def get_initial(self):
        initial = super(RecommendationCreateView, self).get_initial()
        initial["user"] = self.request.user
        initial["book"] = get_object_or_404(Book, slug=self.kwargs.get('slug', None))
        return initial

    def get_context_data(self, **kwargs):
        context = super(RecommendationCreateView, self).get_context_data(**kwargs)
        book = get_object_or_404(Book, slug=self.kwargs.get('slug', None))
        context["the_user"] = self.request.user.get_profile()
        context["recommending"] = True
        context["book"] = \
            process_books([book], self.request.user)[0]
        if self.request.user.get_profile().has_recommended_book(book):
            raise Http404
        return context

class RecommendationDetailsView(DetailView):
    model = Recommendation
    template_name = "books_recommendation_details.html"
    context_object_name = "recommendation"

    def get_context_data(self, **kwargs):
        context = super(RecommendationDetailsView, self).get_context_data(**kwargs)
        book = context["recommendation"].book
        context["book"] = process_books([book], self.request.user)[0]
        return context

class RecommendationDeleteView(DeleteView):
    model = Recommendation
    context_object_name = "recommendation"
    success_url = "/"
    http_method_names = ['post', 'put', 'delete', 'head', 'options', 'trace']

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        msg = "Recommendation was deleted!"
        messages.info(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())


class AddBookView(JSONResponseMixin, AjaxResponseMixin, LoginRequiredMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        r = int(request.POST.get("read", "2"))
        book_id = self.kwargs.get("id")
        print "r -> ", r
        if r < 0:
            self.request.user.get_profile().remove_book(get_object_or_404(Book, pk=book_id))
        else:
            read = bool(r)
            self.request.user.get_profile().add_book(get_object_or_404(Book, pk=book_id), read)
        json_dict = {"result": 1}
        return self.render_json_response(json_dict)
