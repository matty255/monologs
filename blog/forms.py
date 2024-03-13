import json
from django import forms

from .mixins import CustomModelChoiceField
from .models import Post, Comment, Tag, Category
from ajax_select.fields import (
    AutoCompleteSelectMultipleField,
)
from django.core.exceptions import ValidationError
from PIL import Image
from ajax_select import make_ajax_field


class PostAdminForm(forms.ModelForm):
    tags = AutoCompleteSelectMultipleField(
        "tags",
        required=False,
        help_text="태그를 선택하거나 입력하세요.",
        label="Tags",
    )
    category = make_ajax_field(
        Post,
        "category",
        "category",
        help_text="카테고리를 선택하세요.",
        label="Category",
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "summary",
            "thumbnail",
            "author",
            "tags",
            "category",
        ]

    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["tags"].initial = self.instance.tags.all()
            self.fields["category"].initial = self.instance.category

    def save(self, commit=True):
        instance = super(PostAdminForm, self).save(commit=False)

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class PostForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={"class": "tagify-field"}))
    category = CustomModelChoiceField(
        queryset=Category.objects.none(),  # 초기에는 비어 있는 쿼리셋을 설정합니다.
        empty_label="Select Category",
    )

    class Meta:
        model = Post
        fields = ["title", "summary", "content", "tags", "thumbnail", "category"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["content"].widget.attrs.update({"class": "quill-field"})
        if user:

            self.fields["category"].queryset = (
                Category.objects.with_tree_fields().filter(author=user)
            )

    def clean_tags(self):
        tags_str = self.cleaned_data["tags"]
        tags_list = json.loads(tags_str)
        tag_ids = []
        for name in tags_list:
            tag, created = Tag.objects.get_or_create(name=name)
            tag_ids.append(tag.id)
        return tag_ids

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get("thumbnail")
        if thumbnail:
            # 허용된 파일 확장자 목록
            allowed_extensions = ["jpg", "jpeg", "png", "webp"]
            extension = thumbnail.name.split(".")[-1].lower()
            if extension not in allowed_extensions:
                raise ValidationError("지원하지 않는 파일 형식입니다.")

            # 파일 크기 제한 (예: 10MB)
            if thumbnail.size > 10 * 1024 * 1024:  # 10MB
                raise ValidationError(
                    "파일 크기가 너무 큽니다. 10MB 이하의 파일만 업로드해주세요."
                )

        return thumbnail


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
