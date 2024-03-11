from django.contrib import admin
from .models import Post, Tag, Like, Bookmark, Comment, Category
from ajax_select.admin import AjaxSelectAdmin
from ajax_select.fields import autoselect_fields_check_can_add
from .forms import PostAdminForm
from django.core.cache import cache


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

        # 사용자별 카테고리 캐시 키 생성
        cache_key = f"user_{request.user.pk}_categories"
        user_categories = cache.get(cache_key)

        # 캐시에 없으면 데이터베이스에서 조회하고 캐시에 저장
        if not user_categories:
            user_categories = Category.objects.filter(author=request.user)
            cache.set(cache_key, user_categories, 60 * 15)  # 15분 동안 캐시

        form.base_fields["category"].queryset = user_categories

        return form


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ["name"]
