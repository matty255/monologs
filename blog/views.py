from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Post, Comment, Tag, Like, Bookmark
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from .models import Like
from django.db import transaction
from django.shortcuts import get_object_or_404


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


class SearchView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        tag = self.request.GET.get("tag", "")
        post_content_type = ContentType.objects.get_for_model(Post)

        queries = []
        if query:
            queries.append(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(summary__icontains=query)
            )

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


class PostListView(ListView):
    model = Post
    template_name = "blog/blog_list.html"
    context_object_name = "posts"
    paginate_by = 10

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

        context["meta"] = {
            "title": "nonologs" + "|" + post.title,
            "description": post.summary if post.summary else "welcome to monologs",
            "image": (
                self.request.build_absolute_uri(post.thumbnail.url)
                if post.thumbnail
                else ""
            ),
        }

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

        comments = post.comments.filter(parent__isnull=True)
        for comment in comments:
            comment.replies_list = comment.replies.all()

        context["tags"] = post.tags.all()
        context["comments"] = comments
        context["comment_form"] = CommentForm()

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("blog_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        context["tags_list"] = list(Tag.objects.all().values_list("name", flat=True))
        if self.object:
            context["post_tags"] = list(self.object.tags.values_list("name", flat=True))
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog_list")


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/include/comment_form.html"

    def get_success_url(self):
        return reverse_lazy("blog_detail", kwargs={"pk": self.object.post.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs.get("post_pk"))

        parent_id = self.request.POST.get("parent_id")
        if parent_id:
            form.instance.parent = get_object_or_404(Comment, id=parent_id)
            parent_comment = form.instance.parent
            if parent_comment.parent is not None:
                form.instance.parent = parent_comment.parent

        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/include/comment_form.html"

    def get_success_url(self):
        return reverse_lazy("blog_detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/include/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("blog_detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author