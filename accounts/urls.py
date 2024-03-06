from django.urls import path

from .views import (
    FollowToggleView,
    PrivateProfileView,
    PublicProfileView,
    CustomLoginView,
    CustomLogoutView,
)


urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", PrivateProfileView.as_view(), name="private_profile"),
    path("profile/<slug:slug>/", PublicProfileView.as_view(), name="public_profile"),
    path("profile/<int:pk>/follow/", FollowToggleView.as_view(), name="follow_toggle"),
]
