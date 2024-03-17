from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Post, Comment, Tag, Like, Bookmark, Category
from accounts.models import Follow
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from PIL import Image
import io
from django.core.files.base import ContentFile
from main.mixins import Custom404Mixin, UserIsAuthorMixin
from django.http import Http404
from .mixins import LikeMixin, BookmarkMixin
from django.shortcuts import redirect


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


class SearchView(Custom404Mixin, ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        tag = self.request.GET.get("tag", "")
        category_id = self.request.GET.get("category_id", "")
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

        if category_id:
            queries.append(Q(category_id=category_id))

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
        context["tags"] = self.request.GET.get("tag", "")
        return context


class PostListView(Custom404Mixin, ListView):
    model = Post
    template_name = "blog/blog_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("tags").order_by(
            "-created_at"
        )  # Assuming 'created_at' is your datetime field

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["search_fields"] = self.request.GET.getlist("fields", [])
        context["tags"] = self.request.GET.get("tag", "")
        return context


# PostDetailView 정의
class PostDetailView(Custom404Mixin, LikeMixin, BookmarkMixin, DetailView):
    model = Post
    template_name = "blog/blog_detail.html"
    custom_404_message = "포스트를 찾을 수 없습니다."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        user = self.request.user

        # 포스트의 저자 정보
        context["author_profile_picture_url"] = (
            post.author.profile_picture.file.url
            if post.author.profile_picture
            else None
        )
        context["author_profile_status"] = post.author.profile_status

        # 현재 사용자가 포스트의 저자를 팔로우하고 있는지 여부
        context["is_following"] = False
        if user.is_authenticated:
            context["is_following"] = Follow.objects.filter(
                follower=user, following=post.author
            ).exists()

        # 메타 정보 설정
        context["meta"] = {
            "title": "monologs" + "|" + post.title,
            "description": post.summary if post.summary else "welcome to monologs",
            "image": (
                self.request.build_absolute_uri(post.thumbnail.url)
                if post.thumbnail
                else ""
            ),
        }

        context["liked"] = self.get_like_status(user, post)
        context["bookmarked"] = self.get_bookmark_status(user, post)

        context["like_count"] = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(Post), object_id=post.id
        ).count()

        comments = post.comments.filter(parent__isnull=True).prefetch_related("replies")
        for comment in comments:
            comment.liked = self.get_like_status(user, comment)
            comment.bookmarked = self.get_bookmark_status(user, comment)
            comment.author_profile_picture_url = (
                comment.author.profile_picture.file.url
                if comment.author.profile_picture
                else None
            )
            comment.author_profile_status = comment.author.profile_status

            comment.replies_list = comment.replies.all()
            for reply in comment.replies_list:
                reply.author_profile_picture_url = (
                    reply.author.profile_picture.file.url
                    if reply.author.profile_picture
                    else None
                )
                reply.author_profile_status = reply.author.profile_status

        context["tags"] = post.tags.all()
        context["comments"] = comments
        context["comment_form"] = CommentForm()

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("blog_list")

    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags_list"] = list(Tag.objects.all().values_list("name", flat=True))
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        thumbnail = form.cleaned_data.get("thumbnail")
        if thumbnail:
            img = Image.open(thumbnail)
            if img.format != "WEBP":
                output = io.BytesIO()
                img.save(output, format="WEBP")
                output.seek(0)
                thumbnail_name = thumbnail.name.split(".")[0] + ".webp"

                form.instance.thumbnail.save(
                    thumbnail_name, ContentFile(output.read()), save=False
                )

        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.save()
            form.save_m2m()
        return super().form_valid(form)


class PostUpdateView(UserIsAuthorMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_update.html"
    success_url = reverse_lazy("blog_list")

    def get_form_kwargs(self):
        kwargs = super(PostUpdateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags_list"] = list(Tag.objects.all().values_list("name", flat=True))
        if self.object:
            context["post_tags"] = list(self.object.tags.values_list("name", flat=True))
            context["category"] = (
                self.object.category
                if self.object.category
                else Category.objects.filter(
                    name="all", author=self.request.user
                ).first()
            )
        return context

    def form_valid(self, form):
        thumbnail = form.cleaned_data.get("thumbnail")
        if thumbnail:
            img = Image.open(thumbnail)
            if img.format != "WEBP":
                output = io.BytesIO()
                img.save(output, format="WEBP")
                output.seek(0)
                thumbnail_name = thumbnail.name.split(".")[0] + ".webp"

                form.instance.thumbnail.save(
                    thumbnail_name, ContentFile(output.read()), save=False
                )

        response = super().form_valid(form)
        return response


class PostDeleteView(UserIsAuthorMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/include/post_confirm_delete.html"
    success_url = reverse_lazy("blog_list")

    def get_object(self, queryset=None):
        obj = super(PostDeleteView, self).get_object()
        if not obj.author == self.request.user:
            raise HttpResponseForbidden()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.get_object()
        return context


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


class CommentUpdateView(
    UserIsAuthorMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = Comment
    form_class = CommentForm
    template_name = "blog/include/comment_update_form.html"

    def get_success_url(self):
        return reverse_lazy("blog_detail", kwargs={"pk": self.object.post.pk})

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if comment.post is None or comment.author is None:
            raise Http404("댓글이 삭제되었거나 유효하지 않습니다.")
        return comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        context["comment_pk"] = comment.parent.id if comment.parent else comment.id
        context["comment"] = comment
        return context


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "blog/include/comment_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # 댓글의 is_deleted 상태를 True로 설정하고, 내용을 변경
        self.object.is_deleted = True
        self.object.content = "댓글이 삭제되었습니다."
        self.object.save()

        messages.success(request, "댓글이 성공적으로 삭제되었습니다.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        # 댓글이 속한 게시물로 리다이렉트
        return reverse_lazy("blog_detail", kwargs={"pk": self.object.post.pk})
