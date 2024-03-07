from django.contrib.contenttypes.models import ContentType
from .models import CustomUser
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post, Like, Bookmark
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import CustomUser
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm, CustomUserCreationForm, UserProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, UpdateView


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
            if request.user.following.filter(id=user_to_toggle.id).exists():
                request.user.following.remove(user_to_toggle)
                messages.success(
                    request, f"You have unfollowed {user_to_toggle.username}."
                )
            else:
                request.user.following.add(user_to_toggle)
                messages.success(
                    request, f"You are now following {user_to_toggle.username}."
                )

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


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
        context["is_following"] = self.request.user.following.filter(
            id=user.id
        ).exists()
        return context


class PrivateProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = "accounts/private_profile.html"
    success_url = reverse_lazy("private_profile")

    def get_object(self):

        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        post_content_type = ContentType.objects.get_for_model(Post)

        liked_content_ids = Like.objects.filter(
            user=user, content_type=post_content_type
        ).values_list("object_id", flat=True)
        liked_posts = Post.objects.filter(id__in=liked_content_ids)

        bookmarked_content_ids = Bookmark.objects.filter(
            user=user, content_type=post_content_type
        ).values_list("object_id", flat=True)
        bookmarked_posts = Post.objects.filter(id__in=bookmarked_content_ids)

        context["liked_posts"] = liked_posts
        context["bookmarked_posts"] = bookmarked_posts

        return context


class PublicProfileView(DetailView):
    model = CustomUser
    template_name = "accounts/public_profile.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "slug"
