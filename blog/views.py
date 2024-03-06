from django.views.generic import View, ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Post, Comment, Tag, Like, Bookmark
from .forms import PostForm, CommentForm, ReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from .models import Like
from ajax_select.fields import autoselect_fields_check_can_add
from django.db import transaction
import json


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
    paginate_by = 10  # 한 페이지에 보여줄 객체 수

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        tag = self.request.GET.get("tag", "")
        post_content_type = ContentType.objects.get_for_model(Post)
        if query:
            object_list = self.model.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        elif tag:
            object_list = self.model.objects.filter(tags__name__icontains=tag)
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


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/blog_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["reply_form"] = ReplyForm()
        context["comments"] = self.object.comments.filter(parent__isnull=True)
        context["post"] = self.object

        # Add tags to the context
        context["tags"] = self.object.tags.all()

        content_type = ContentType.objects.get_for_model(Post)
        if self.request.user.is_authenticated:
            liked = Like.objects.filter(
                content_type=content_type,
                object_id=self.object.id,
                user=self.request.user,
            ).exists()
            context["liked"] = liked

            # Check if the user has bookmarked the post
            bookmarked = Bookmark.objects.filter(
                content_type=content_type,
                object_id=self.object.id,
                user=self.request.user,
            ).exists()
            context["bookmarked"] = bookmarked

            # Count of likes for the post, visible to everyone
            context["like_count"] = Like.objects.filter(
                content_type=content_type,
                object_id=self.object.id,
            ).count()

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("blog_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.all().values_list("name", flat=True)
        context["tags_list"] = list(tags)
        return context

    def form_valid(self, form):
        # Start a new transaction
        with transaction.atomic():
            # This calls the save method of the form which will create the new Post object
            form.instance.author = self.request.user
            self.object = form.save(commit=False)

            # Add any additional processing here, such as adding the author if needed
            self.object.author = (
                self.request.user
            )  # Example: setting the author of the post
            self.object.save()

            # Now handle the tags
            tags_data = self.request.POST.get(
                "tags"
            )  # The name 'tags' must match the name in your form input
            tags_list = json.loads(tags_data)

            # Clear any old tags
            self.object.tags.clear()

            # Add new tags
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                self.object.tags.add(tag)

            # Finally save the m2m relationship
            form.save_m2m()

            # The super method returns an HttpResponseRedirect to the success_url
            return super().form_valid(form)


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
