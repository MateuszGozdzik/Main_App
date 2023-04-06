from django import forms
from .models import Quote

class MyModelForm(forms.ModelForm):
    class Meta:
        model = Quote
