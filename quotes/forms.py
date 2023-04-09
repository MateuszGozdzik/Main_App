from django import forms
from .models import Quote
from tinymce.widgets import TinyMCE

INPUT_CLASSES = "w-full py-4 px-6 rounded-xl"


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ("title", "content", "author", "language")

        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "author": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "language": forms.Select(attrs={"class": INPUT_CLASSES}),
            "content": TinyMCE(attrs={"class": INPUT_CLASSES}),
        }


class QuoteFiltersForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ("language",)

        widgets = {
            "language": forms.Select(attrs={"class": INPUT_CLASSES}),
        }
