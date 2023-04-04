from django import forms

class PushupForm100(forms.Form):
    NR = forms.BooleanField(required=False)
    WD = forms.BooleanField(required=False)
    DM = forms.BooleanField(required=False)
    EX = forms.BooleanField(required=False)
    SS = forms.BooleanField(required=False)
    CP = forms.BooleanField(required=False)
    AR = forms.BooleanField(required=False)
    OC = forms.BooleanField(required=False)
    TW = forms.BooleanField(required=False)
    ST = forms.BooleanField(required=False)

    num_sets = forms.IntegerField()
    reps_in_set = forms.IntegerField(required=False)
    total_reps = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        num_sets = cleaned_data.get("num_sets")
        reps_in_set = cleaned_data.get("reps_in_set")

        if num_sets and reps_in_set:
            raise forms.ValidationError("Please choose either number of sets or reps in a set, but not both.")
        elif not num_sets and not reps_in_set:
            raise forms.ValidationError("Please choose either number of sets or reps in a set.")

