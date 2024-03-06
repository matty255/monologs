from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Post, Comment, Tag, Like, Bookmark
from .forms import PostForm, CommentForm, ReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from .models import Like
from django.core.cache import cache
from django.db import transaction
import json
from django.forms.models import model_to_dict


class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        object_id = request.POST.get("object_id")
        content_type = request.POST.get("content_type")
        content_type = ContentType.objects.get(model=content_type)

        model_class = content_type.model_class()
        object_being_liked = model_class.objects.get(pk=object_id)

        if (
            hasattr(object_being_liked, "author")
            and object_being_liked.author == request.user
        ):
            messages.error(request, "You cannot like your own posts or comments.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

        like, created = Like.objects.get_or_create(
            user=request.user, content_type=content_type, object_id=object_id
        )

        if not created:
            like.delete()
            messages.info(request, "Like removed.")
        else:
            messages.success(request, "Successfully liked.")

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class ToggleBookmarkView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseForbidden()

        object_id = request.POST.get("object_id")
        content_type = request.POST.get("content_type")
        content_type = ContentType.objects.get(model=content_type)

        bookmark, created = Bookmark.objects.get_or_create(
            user=user, content_type=content_type, object_id=object_id
        )

        if not created:
            bookmark.delete()

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class PostListView(ListView):
    model = Post
    template_name = "blog/blog_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        search_fields = self.request.GET.getlist("fields", [])
        tag = self.request.GET.get("tag", "")
        post_content_type = ContentType.objects.get_for_model(Post)

        queries = []
        if query:
            if "title" in search_fields:
                queries.append(Q(title__icontains=query))
            if "content" in search_fields:
                queries.append(Q(content__icontains=query))
            if "summary" in search_fields:  # 'summary' 필드가 모델에 존재한다고 가정
                queries.append(Q(summary__icontains=query))

        if tag:
            queries.append(Q(tags__name__icontains=tag))

        if queries:
            combined_query = queries.pop()
            for item in queries:
                combined_query |= item
            object_list = self.model.objects.filter(combined_query)
        else:
            object_list = self.model.objects.all()

        object_list = object_list.annotate(
            like_count=Count(
                "id",
                filter=Q(
                    id__in=Like.objects.filter(content_type=post_content_type).values(
                        "object_id"
                    )
                ),
            )
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["search_fields"] = self.request.GET.getlist("fields", [])
        context["tag"] = self.request.GET.get("tag", "")
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/blog_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.get_object()

        if self.request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(Post)
            user = self.request.user

            liked = Like.objects.filter(
                content_type=content_type, object_id=post.id, user=user
            ).exists()
            context["liked"] = liked

            bookmarked = Bookmark.objects.filter(
                content_type=content_type, object_id=post.id, user=user
            ).exists()
            context["bookmarked"] = bookmarked

            like_count = Like.objects.filter(
                content_type=content_type, object_id=post.id
            ).count()
            context["like_count"] = like_count

        comments = list(
            post.comments.filter(parent__isnull=True).values(
                "id", "content", "created_at"
            )
        )
        context["tags"] = self.object.tags.all()

        context["comments"] = comments

        context["comment_form"] = CommentForm()
        context["reply_form"] = ReplyForm()

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("blog_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch tags directly from the database
        context["tags_list"] = list(Tag.objects.all().values_list("name", flat=True))
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.save()
            form.save_m2m()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_update.html"
    success_url = reverse_lazy("blog_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all tags for autocomplete functionality
        context["tags_list"] = list(Tag.objects.all().values_list("name", flat=True))
        # Get a list of names of tags associated with this specific post
        if self.object:
            context["post_tags"] = list(self.object.tags.values_list("name", flat=True))
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/include/comment_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blog_detail", kwargs={"pk": self.kwargs["pk"]})


class ReplyCreateView(CreateView):
    model = Comment
    form_class = ReplyForm
    template_name = "blog/include/reply_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs["post_pk"])
        form.instance.parent = Comment.objects.get(pk=self.kwargs["comment_pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blog_detail", kwargs={"pk": self.kwargs["post_pk"]})
