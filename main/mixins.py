from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin


class UserIsAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class Custom404Mixin:
    custom_404_message = None

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:

            message = self.custom_404_message or "페이지를 찾을 수 없습니다."
            context = {"message": message}
            return render(request, "custom_404.html", context, status=404)
