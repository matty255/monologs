from django.urls import path
from .views import (
    SearchView,
    PostListView,
    PostDetailView,
    ToggleLikeView,
    ToggleBookmarkView,
    PostCreateView,
    PostUpdateView,
    CommentCreateView,
    PostDeleteView,
    CommentUpdateView,
    CommentDeleteView,
)


urlpatterns = [
    path("", PostListView.as_view(), name="blog_list"),
    path("search/", SearchView.as_view(), name="search"),
    path("<int:pk>/", PostDetailView.as_view(), name="blog_detail"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("update/<int:pk>/", PostUpdateView.as_view(), name="post_update"),
    path("delete/<int:pk>/", PostDeleteView.as_view(), name="post_delete"),
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
    path(
        "comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment_update"
    ),
    path(
        "comment/<int:pk>/delete/",
        CommentDeleteView.as_view(),
        name="comment_delete",
    ),
]
