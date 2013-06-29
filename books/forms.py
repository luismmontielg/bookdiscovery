from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User

from .models import UserProfile, Book, Recommendation


class BookForm(forms.ModelForm):
    class Meta:
        model = Book


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("bio",)


class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ("review", "tags", "book", "user")

    def __init__(self, **kwargs):
        super(RecommendationForm, self).__init__(**kwargs)
        self.fields['book'].widget = forms.HiddenInput()
        self.fields['user'].widget = forms.HiddenInput()

    def clean(self):
        self.cleaned_data = super(RecommendationForm, self).clean()
        book = self.cleaned_data["book"]
        user = self.cleaned_data["user"]
        categories = book.categories.all()
        if not user.get_profile().can_recommend_book(book):
            raise ValidationError("You must have read at least 2 books on this topic before submitting a recommendation.")
        return self.cleaned_data
