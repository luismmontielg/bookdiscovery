from django.views.generic import ListView, DetailView

from .models import Book, Author, Category


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
