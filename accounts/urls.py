from django.urls import path

from .views import (
    CategoryCreateView,
    FollowToggleView,
    PrivateProfileView,
    PublicProfileView,
    CustomLoginView,
    CustomLogoutView,
    RegisterView,
    UploadAndCropView,
    ProfileImageDeleteView,
    UserDeleteView,
    UserFollowingListView,
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", PrivateProfileView.as_view(), name="private_profile"),
    path("crop-image/", UploadAndCropView.as_view(), name="upload_and_crop"),
    path(
        "profile/delete_image/",
        ProfileImageDeleteView.as_view(),
        name="profile_image_delete",
    ),
    path("profile/<int:pk>/follow/", FollowToggleView.as_view(), name="follow_toggle"),
    path(
        "follow_list/<int:id>/",
        UserFollowingListView.as_view(),
        name="follow_list",
    ),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),
    path("category/create/", CategoryCreateView.as_view(), name="category_create"),
]
