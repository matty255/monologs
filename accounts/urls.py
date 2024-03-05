from django.urls import path
from .views import PrivateProfileView, PublicProfileView


urlpatterns = [
    path("profile/", PrivateProfileView.as_view(), name="private_profile"),
    path("profile/<slug:slug>/", PublicProfileView.as_view(), name="public_profile"),
]
