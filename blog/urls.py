from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    ToggleLikeView,
    ToggleBookmarkView,
    PostCreateView,
    PostUpdateView,
    CommentCreateView,
)


urlpatterns = [
    path("", PostListView.as_view(), name="blog_list"),
    path("<int:pk>/", PostDetailView.as_view(), name="blog_detail"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("update/<int:pk>/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/toggle_like/", ToggleLikeView.as_view(), name="toggle_like"),
    path(
        "post/<int:pk>/toggle_bookmark/",
        ToggleBookmarkView.as_view(),
        name="toggle_bookmark",
    ),
    path(
        "post/<int:post_pk>/comment/",
        CommentCreateView.as_view(),
        name="comment_create",
    ),
]
