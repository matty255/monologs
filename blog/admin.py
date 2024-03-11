from django.contrib import admin
from .models import Post, Tag, Like, Bookmark, Comment, Category
from ajax_select.admin import AjaxSelectAdmin
from ajax_select.fields import autoselect_fields_check_can_add
from .forms import PostAdminForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]
    search_fields = ["name"]


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
class PostAdmin(AjaxSelectAdmin):
    form = PostAdminForm
    list_display = ["title", "author", "category", "created_at"]
    search_fields = ["title", "content"]
    list_filter = ["created_at", "category"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        autoselect_fields_check_can_add(form, self.model, request.user)

        return form


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ["name"]
