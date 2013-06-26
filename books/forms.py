from itertools import chain
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

from django.conf import settings
from django import forms
from django.template import Context, loader
from django.utils.safestring import SafeString

from django.forms import CharField, ChoiceField, Select,\
        RadioSelect, CheckboxSelectMultiple, MultipleChoiceField,\
        CheckboxInput
from django.forms import ValidationError
from django.forms.forms import BoundField

from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.files.images import get_image_dimensions
from django.contrib.auth.models import User


class BookForm(forms.ModelForm):
    class Meta:
        model = Book

class BookSearchForm(forms.ModelForm):
