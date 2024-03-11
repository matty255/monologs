from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, CroppedImage
from blog.models import Category
from django.utils.translation import gettext_lazy as _
from PIL import Image


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


class ImageUploadForm(forms.Form):
    # 여기서 'file'은 사용자로부터 이미지를 받는 필드의 이름입니다.
    file = forms.ImageField()

    def clean_file(self):
        file = self.cleaned_data["file"]

        # 허용된 파일 확장자 목록
        allowed_extensions = ["jpg", "jpeg", "png", "webp"]
        extension = file.name.split(".")[-1].lower()
        if extension not in allowed_extensions:
            raise ValidationError("지원하지 않는 파일 형식입니다.")

        # 움직이는 이미지(GIF) 검사를 추가할 수 있습니다.
        if extension == "gif":
            try:
                with Image.open(file) as img:
                    if img.is_animated:
                        raise ValidationError("움직이는 GIF는 허용되지 않습니다.")
            except IOError:
                raise ValidationError("이미지 파일을 읽는 중 오류가 발생했습니다.")

        return file


class CategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=Category.objects.none(),  # 자바스크립트로 동적으로 채워짐
        required=False,
        empty_label="Select Parent Category (Leave blank for root)",
        label="Parent Category",
    )

    class Meta:
        model = Category
        fields = ["name", "parent"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        if user is not None:
            # 'parent' 선택을 위한 쿼리셋.
            self.fields["parent"].queryset = Category.objects.filter(author=user)
