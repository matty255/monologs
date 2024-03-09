# urls.py
from django.urls import path
from .views import IndexView, AboutView, ConvertAndDownloadView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path(
        "download_image/<int:pk>/",
        ConvertAndDownloadView.as_view(),
        name="convert_and_download",
    ),
]
