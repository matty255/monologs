from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    CommentCreateView,
    ReplyCreateView,
    ToggleLikeView,
    ToggleBookmarkView,
    PostCreateView,
)


urlpatterns = [
    path("", PostListView.as_view(), name="blog_list"),
    path("<int:pk>/", PostDetailView.as_view(), name="blog_detail"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/toggle_like/", ToggleLikeView.as_view(), name="toggle_like"),
    path(
        "post/<int:pk>/toggle_bookmark/",
        ToggleBookmarkView.as_view(),
        name="toggle_bookmark",
    ),
    path("<int:pk>/comment/", CommentCreateView.as_view(), name="comment_create"),
    path(
        "<int:post_pk>/comment/<int:comment_pk>/reply/",
        ReplyCreateView.as_view(),
        name="reply_create",
    ),
]
