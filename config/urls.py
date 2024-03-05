from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


from config import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("accounts/", include("accounts.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    path("ajax_select/", include("ajax_select.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
