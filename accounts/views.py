from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from .models import CustomUser
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post, Like, Bookmark


class PrivateProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/private_profile.html"

    def get_context_data(self, **kwargs):
        context = super(PrivateProfileView, self).get_context_data(**kwargs)
        user = self.request.user

        # Fetch the ContentType for the Post model
        post_content_type = ContentType.objects.get_for_model(Post)

        # Fetch the liked posts for the current user
        liked_content_ids = Like.objects.filter(
            user=user, content_type=post_content_type
        ).values_list("object_id", flat=True)
        liked_posts = Post.objects.filter(id__in=liked_content_ids)

        # Fetch the bookmarked posts for the current user
        bookmarked_content_ids = Bookmark.objects.filter(
            user=user, content_type=post_content_type
        ).values_list("object_id", flat=True)
        bookmarked_posts = Post.objects.filter(id__in=bookmarked_content_ids)

        context["private_profile"] = user
        context["liked_posts"] = liked_posts
        context["bookmarked_posts"] = bookmarked_posts

        return context


class PublicProfileView(DetailView):
    model = CustomUser
    template_name = "accounts/public_profile.html"
    context_object_name = "profile_user"
    slug_field = "username"  # 또는 'slug', 사용자 모델에 따라 달라질 수 있음
    slug_url_kwarg = "slug"
