from django.contrib import admin
from .models import Post, Rate


class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "created_at"]
    search_fields = ["title", "author__username"]
    list_filter = ["created_at"]


admin.site.register(Post, PostAdmin)


class RateAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post", "score", "created_at"]
    search_fields = ["user__username", "post__title"]
    list_filter = ["created_at"]


admin.site.register(Rate, RateAdmin)
