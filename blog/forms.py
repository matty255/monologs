import json
from django import forms
from .models import Post, Comment, Tag
from ajax_select.fields import (
    AutoCompleteSelectField,
    AutoCompleteSelectMultipleField,
    autoselect_fields_check_can_add,
)


class PostAdminForm(forms.ModelForm):
    tags = AutoCompleteSelectMultipleField(
        "tags",
        required=False,
        help_text="태그를 선택하거나 입력하세요.",
        label="Tags",
    )

    class Meta:
        model = Post
        fields = ["title", "content", "author", "tags"]

    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)
        # If the instance already exists (e.g., during edit), initialize the tags field.
        if self.instance.pk:
            self.fields["tags"].initial = self.instance.tags.all()

    def save(self, commit=True):
        instance = super(PostAdminForm, self).save(commit=False)

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class PostForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={"class": "tagify-field"}))

    class Meta:
        model = Post
        fields = ["title", "summery", "content", "tags"]  # Removed 'author'

    def clean_tags(self):
        tags_str = self.cleaned_data["tags"]
        tags_list = json.loads(tags_str)
        # Convert tag names to tag IDs
        tag_ids = []
        for name in tags_list:
            tag, created = Tag.objects.get_or_create(name=name)
            tag_ids.append(tag.id)
        return tag_ids


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
