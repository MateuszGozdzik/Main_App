from django import forms
from .models import Quote
from tinymce.widgets import TinyMCE

INPUT_CLASSES = "w-full py-4 px-6 rounded-xl"
CHECKBOX_CLASSES = (
    "absolute block w-6 h-6 rounded-full bg-white border-4 cursor-pointer right-0 top-0"
)


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ("title", "content", "author", "language")

        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASSES, "required": True}),
            "author": forms.TextInput(attrs={"class": INPUT_CLASSES, "required": True}),
            "language": forms.Select(attrs={"class": INPUT_CLASSES, "required": True}),
            "content": TinyMCE(attrs={"class": INPUT_CLASSES}),
        }


class QuoteSearchForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ("title", "content", "author", "language")

        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "author": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "language": forms.Select(attrs={"class": INPUT_CLASSES}),
            "content": forms.TextInput(attrs={"class": INPUT_CLASSES}),
        }

    is_favorite = forms.BooleanField(
        label="Is favorite",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": CHECKBOX_CLASSES}),
    )
    added_by_current_user = forms.BooleanField(
        label="Added by me",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": CHECKBOX_CLASSES}),
    )

    def search(self, user, get_all_quotes):
        # Build a queryset with the selected filters
        queryset = get_all_quotes(user)
        if self.cleaned_data["title"]:
            queryset = queryset.filter(title__iregex=self.cleaned_data["title"])
        if self.cleaned_data["content"]:
            queryset = queryset.filter(content__iregex=self.cleaned_data["content"])
        if self.cleaned_data["author"]:
            queryset = queryset.filter(author__iregex=self.cleaned_data["author"])
        if self.cleaned_data["language"]:
            queryset = queryset.filter(language=self.cleaned_data["language"])
        if self.cleaned_data["is_favorite"]:
            queryset = queryset.filter(favorites=user)
        if self.cleaned_data["added_by_current_user"]:
            queryset = queryset.filter(user=user)

        # Return a random quote from the resulting queryset
        return queryset.order_by("?").first()
