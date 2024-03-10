from django.contrib.contenttypes.models import ContentType
from .models import CustomUser
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post, Like, Bookmark
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import CustomUser, Follow
from django.contrib.auth.views import LoginView
from .forms import (
    CustomLoginForm,
    CustomUserCreationForm,
    UserProfileForm,
    ImageUploadForm,
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login
from django.views.generic import CreateView, UpdateView, ListView
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from PIL import Image
import io
from django.core.files.base import ContentFile
from datetime import datetime
from .mixins import UploadToPathMixin


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("private_profile")
    template_name = "accounts/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Registration failed. Please check the form.")
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy("blog_list")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("blog_list")

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.get_next_page())

    def get_next_page(self):
        next_page = self.request.GET.get("next")
        return next_page or super().get_next_page()

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class FollowToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_to_toggle = get_object_or_404(CustomUser, pk=kwargs.get("pk"))

        if user_to_toggle == request.user:
            messages.error(request, "You cannot follow yourself.")
        else:
            if request.user.following.filter(following=user_to_toggle).exists():
                # Unfollow
                follow_instance = Follow.objects.get(
                    follower=request.user, following=user_to_toggle
                )
                follow_instance.delete()
                messages.success(
                    request, f"You have unfollowed {user_to_toggle.username}."
                )
            else:
                # Follow
                follow_instance = Follow.objects.create(
                    follower=request.user, following=user_to_toggle
                )
                messages.success(
                    request, f"You are now following {user_to_toggle.username}."
                )

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class UserFollowingListView(LoginRequiredMixin, ListView):
    template_name = "accounts/include/user_following_list.html"
    context_object_name = "following_users"

    def get_queryset(self):
        user_info = self.kwargs.get("username")
        user = get_object_or_404(CustomUser, username=user_info)
        return user.following.all()


class FollowingListView(LoginRequiredMixin, ListView):
    template_name = "accounts/include/following_list.html"
    context_object_name = "following_users"

    def get_queryset(self):
        return self.request.user.following.all()


class PublicProfileView(DetailView):
    model = CustomUser
    template_name = "accounts/public_profile.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["following"] = user.following.all()
        context["followers"] = user.followers.all()
        context["is_following"] = (
            self.request.user.is_authenticated
            and self.request.user.following.filter(id=user.id).exists()
        )
        return context


class ProfileImageDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.profile_picture:
            user.profile_picture.delete()
            user.profile_picture = None
            user.save()
        return redirect("private_profile")


class PrivateProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    second_form_class = ImageUploadForm
    template_name = "accounts/private_profile.html"
    success_url = reverse_lazy("private_profile")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "image_form" not in context:
            context["image_form"] = (
                self.second_form_class()
            )  # 이미지 업로드 폼을 컨텍스트에 추가
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        image_form = self.second_form_class(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():

            cropped_image = image_form.save()
            user = request.user
            if user.profile_picture:
                user.profile_picture.delete()
            user.profile_picture = cropped_image
            user.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class UploadAndCropView(LoginRequiredMixin, View):
    form_class = ImageUploadForm
    template_name = "accounts/include/crop.html"
    login_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            if user.profile_picture:
                user.profile_picture.delete()  # Delete existing picture

            cropped_image = form.save(commit=False)
            cropped_image.user = user  # Assuming the model has a user field to link to

            # Convert the image to WebP
            image_content = cropped_image.file.read()
            image = Image.open(io.BytesIO(image_content))
            webp_image = io.BytesIO()
            image.save(webp_image, format="WEBP")
            webp_image.seek(0)

            # Apply custom file path based on user and date
            webp_filename = UploadToPathMixin.upload_to_user_path(
                cropped_image,
                f"{user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.webp",
                "cropped_images",
            )
            cropped_image.file.save(
                webp_filename, ContentFile(webp_image.read()), save=False
            )
            cropped_image.save()

            user.profile_picture = cropped_image
            user.save()

            image_url = cropped_image.file.url
            return JsonResponse(
                {
                    "message": "Profile picture updated successfully.",
                    "imageUrl": image_url,
                    "imageId": cropped_image.id,
                }
            )

        return render(request, self.template_name, {"form": form})


class DeleteProfilePictureView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = get_object_or_404(CustomUser, pk=user_id)
        if user.profile_picture:
            user.profile_picture.delete()
            user.profile_picture = None
            user.save()
            messages.success(request, "Profile picture deleted.")
        else:
            messages.info(request, "No profile picture to delete.")
        return HttpResponseRedirect(reverse("admin:index"))


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = "accounts/user_confirm_delete.html"
    success_url = reverse_lazy("index")  # 탈퇴 성공 후 리다이렉트될 URL

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user


class PublicProfileView(DetailView):
    model = CustomUser
    template_name = "accounts/public_profile.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "slug"
