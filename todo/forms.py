from django import forms
from .models import Todo


INPUT_CLASSES = "w-full py-4 px-6 rounded-xl"


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ("title", "deadline")

        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASSES, "required": True}),
            "deadline": forms.DateInput(attrs={"class": INPUT_CLASSES, "type": "date"}),
        }
