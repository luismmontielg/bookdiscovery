# Create your views here.
from django.views.generic import TemplateView

class HomeView(TemplateView):
    tempalte_name = "books_index.html"
