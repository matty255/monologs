# urls.py
from django.urls import path
from .views import (
    IndexView,
    AboutView,
    ConvertAndDownloadView,
    ConvertAndDownloadPNGView,
)
from accounts.views import PublicProfileView, UserCategoriesView, PublicCategoryTreeView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path(
        "download_image/<int:pk>/",
        ConvertAndDownloadView.as_view(),
        name="convert_and_download",
    ),
    path(
        "download_image_png/<int:pk>/",
        ConvertAndDownloadPNGView.as_view(),
        name="convert_and_download_png",
    ),
    path("@<str:slug>/", PublicProfileView.as_view(), name="public_profile"),
    # path(
    #     "@<str:username>/category/",
    #     PublicCategoryTreeView.as_view(),
    #     name="public-profile-category",
    # ),
    # path(
    #     "@<str:username>/category/<int:category_id>/",
    #     PublicCategoryTreeView.as_view(),
    #     name="public-profile-category",
    # ),
]
