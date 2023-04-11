from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


INPUT_CLASSES = "w-full py-4 px-6 rounded-xl"

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your username",
                "class": INPUT_CLASSES,
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Your password",
                "class": INPUT_CLASSES,
            }
        )
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your username",
                "class": INPUT_CLASSES,
            }
        )
    )

    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Your email address",
                "class": INPUT_CLASSES,
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Your password",
                "class": INPUT_CLASSES,
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat password",
                "class": INPUT_CLASSES,
            }
        )
    )


class GravatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("gravatar_link",)

        widgets = {
            "gravatar_link": forms.URLInput(attrs={"class": INPUT_CLASSES}),
        }


class ProfileSection1Form(forms.ModelForm):
    public = forms.ChoiceField(
        choices=((True, "Public"), (False, "Private")), widget=forms.RadioSelect
    )

    def clean_username(self):
        current_user = self.instance
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exclude(pk=current_user.pk).exists():
            raise forms.ValidationError(
                "This username is already taken. Please choose a different one."
            )
        return username

    def clean_email(self):
        current_user = self.instance
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=current_user.pk).exists():
            raise forms.ValidationError(
                "This email is already registered. Please use a different one."
            )
        return email

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

        widgets = {
            "first_name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "last_name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "username": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "email": forms.EmailInput(attrs={"class": INPUT_CLASSES, "required": True}),
        }

    def __init__(self, *args, **kwargs):
        try:
            public_bool = kwargs.pop("public_bool")
        except:
            public_bool = None

        super(ProfileSection1Form, self).__init__(*args, **kwargs)
        if public_bool != None:
            self.fields["public"].initial = public_bool


class ProfileSection2Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ()

    quote_newsletter = forms.ChoiceField(
        choices=((True, "Yes"), (False, "No")),
        widget=forms.RadioSelect,
    )
    email_notifications = forms.ChoiceField(
        choices=((True, "Yes"), (False, "No")), widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        try:
            quote_bool = kwargs.pop("quote_bool")
        except:
            quote_bool = None

        try:
            email_bool = kwargs.pop("email_bool")
        except:
            email_bool = None

        super(ProfileSection2Form, self).__init__(*args, **kwargs)
        if quote_bool != None:
            self.fields["quote_newsletter"].initial = quote_bool
        if email_bool != None:
            self.fields["email_notifications"].initial = email_bool
