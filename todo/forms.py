from django import forms
from .models import Todo


INPUT_CLASSES = "w-full py-4 px-6 rounded-xl"


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ("title", "content")

        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASSES, "required": True}),
            "content": forms.TextInput(attrs={"class": INPUT_CLASSES}),
        }
