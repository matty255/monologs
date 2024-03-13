from django.contrib.contenttypes.models import ContentType
from .models import CustomUser
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post, Like, Comment, Category
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import CustomUser, Follow
from django.contrib.auth.views import LoginView
from .forms import (
    CategoryForm,
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
from main.mixins import UserIsAuthorMixin
from .mixins import LikedAndBookmarkedMixin

import json
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.db import transaction
import logging


logger = logging.getLogger(__name__)


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
        return user.following.all().select_related("profile_picture")


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

    def get_profile_image_url(self, user):
        if user.profile_picture:
            return self.request.build_absolute_uri(user.profile_picture.url)
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        category_id = self.kwargs.get("category_id")
        all_categories = Category.objects.filter(author=user).values(
            "id", "name", "parent_id"
        )

        if category_id:
            selected_category = get_object_or_404(Category, pk=category_id, author=user)
            category_ids = [selected_category.id] + list(
                selected_category.descendants(include_self=False).values_list(
                    "id", flat=True
                )
            )
            posts = Post.objects.filter(category_id__in=category_ids, author=user)

            # 카테고리가 선택된 경우, 메타 정보 설정
            context["meta"] = {
                "title": f"monologs | {selected_category.name}",
                "description": f"{user.username} 닙의 category:  {selected_category.name}",
                "image": self.get_profile_image_url(user),
            }
        else:
            posts = Post.objects.filter(author=user)
            # 기본 메타 정보 설정
            context["meta"] = {
                "title": "monologs | Profile",
                "description": f"{user.username} 닙의 글을 monologs에서 더 찾아보세요.",
                "image": self.get_profile_image_url(user),
            }

        context["categories"] = all_categories
        context["posts"] = posts
        context["selected_category_id"] = category_id
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


class PrivateProfileView(LoginRequiredMixin, UpdateView, LikedAndBookmarkedMixin):
    model = CustomUser
    form_class = UserProfileForm
    second_form_class = ImageUploadForm
    template_name = "accounts/private_profile.html"
    success_url = reverse_lazy("private_profile")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # 믹스인을 사용하여 좋아요 및 북마크한 Post와 Comment 정보를 가져옴
        liked_and_bookmarked_context = self.get_liked_and_bookmarked_objects(
            user, [Post, Comment]
        )
        context.update(liked_and_bookmarked_context)

        if "image_form" not in context:
            context["image_form"] = self.second_form_class()

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


class UserDeleteView(
    LoginRequiredMixin, UserIsAuthorMixin, UserPassesTestMixin, DeleteView
):
    model = CustomUser
    template_name = "accounts/user_confirm_delete.html"
    success_url = reverse_lazy("index")  # 탈퇴 성공 후 리다이렉트될 URL


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "accounts/category_create.html"
    success_url = reverse_lazy("category_list")

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():  # 모든 작업을 하나의 트랜잭션으로 묶습니다.
                tree_data = json.loads(request.POST.get("tree"))
                username = request.POST.get("username")
                user = CustomUser.objects.get(username=username)
                created_nodes = []

                for node in tree_data:
                    parent_id = self.get_parent_id(node)

                    if not node["id"].isdigit():
                        cat = Category.objects.create(
                            name=node["text"],
                            parent_id=parent_id,
                            author=user,
                        )
                        created_nodes.append({"temp_id": node["id"], "new_id": cat.id})
                    else:
                        cat, created = Category.objects.update_or_create(
                            id=int(node["id"]) if node["id"].isdigit() else None,
                            defaults={
                                "name": node["text"],
                                "parent_id": parent_id,
                                "author": user,
                            },
                        )

                return JsonResponse(
                    {"status": "success", "created_nodes": created_nodes}
                )

        except ValidationError as e:
            logger.error("Validation Error: %s", e)
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        except Exception as e:
            logger.error("Unexpected Error: %s", e, exc_info=True)
            return JsonResponse(
                {"status": "error", "message": "An unexpected error occurred."},
                status=500,
            )

    def get_parent_id(self, node):
        # 부모 ID를 추출하는 별도의 메서드를 정의할 수 있습니다.
        parent_id = node.get("parent")
        if parent_id and parent_id != "#":
            if parent_id.isdigit():
                return int(parent_id)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.with_tree_fields()
        # jsTree 형식에 맞게 데이터를 변환합니다.
        context["tree"] = json.dumps(
            [
                {
                    "id": cat.id,
                    "parent": "#" if cat.parent_id is None else cat.parent_id,
                    "text": cat.name,
                }
                for cat in categories
            ]
        )
        return context


class UserCategoriesView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"error": "User is not authenticated"}, status=401)

        cache_key = f"user_{user.pk}_category"
        categories = cache.get(cache_key)

        if categories is None:
            categories = list(
                Category.objects.filter(author=user).values("id", "name", "parent_id")
            )
            cache.set(cache_key, categories, 60 * 15)  # 캐시에 15분간 저장

        return JsonResponse({"categories": categories})
