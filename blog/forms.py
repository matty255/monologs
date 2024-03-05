from django import forms
from .models import Post, Comment
from ajax_select.fields import AutoCompleteSelectMultipleField


# Now let's make sure our PostForm uses the AutoCompleteSelectMultipleField correctly
class PostForm(forms.ModelForm):
    tags = AutoCompleteSelectMultipleField(
        "tags",  # 'tags' is the name of the lookup defined in lookups.py
        required=False,
        help_text="태그를 선택하거나 입력하세요.",
        label="Tags",
    )

    class Meta:
        model = Post
        fields = ["title", "content", "author", "tags"]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # If the instance already exists (e.g., during edit), initialize the tags field.
        if self.instance.pk:
            self.fields["tags"].initial = self.instance.tags.all()

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)

        if commit:
            instance.save()
            # For ManyToMany fields, you must save the instance then set the relation.
            self.save_m2m()

        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
