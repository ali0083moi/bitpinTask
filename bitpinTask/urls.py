from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/posts/", include("posts.urls", namespace="posts")),
    path("api/auth/", include("accounts.urls", namespace="accounts")),
]
