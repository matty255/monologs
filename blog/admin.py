from django.contrib import admin
from .models import Post, Tag, Like, Bookmark
from ajax_select.admin import AjaxSelectAdmin
from ajax_select.fields import autoselect_fields_check_can_add
from .forms import PostForm


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Post)
class PostAdmin(AjaxSelectAdmin):  # Inherit from AjaxSelectAdmin
    form = PostForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # This utility function will check for permissions and enable the green + button
        autoselect_fields_check_can_add(form, self.model, request.user)

        return form
