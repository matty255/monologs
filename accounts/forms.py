from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, CroppedImage
from django.utils.translation import gettext_lazy as _


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"autocomplete": "email"})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords must match."))

        self.validate_password_strength(password1)
        return password2

    def validate_password_strength(self, password):
        if len(password) < 8:
            raise ValidationError(
                _("비밀번호가 너무 짧습니다. 최소 8 문자를 포함해야 합니다.")
            )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = []


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = CroppedImage
        fields = ("file",)
