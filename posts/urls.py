from django.urls import path
from .views import AddScoreView, RecievePostsView, RecievePostDetailView, AddPostView

app_name = "posts"

urlpatterns = [
    path("add-score/", AddScoreView.as_view(), name="add-score"),
    path("posts/", RecievePostsView.as_view(), name="posts-list"),
    path("posts/<int:pk>/", RecievePostDetailView.as_view(), name="posts-detail"),
    path("add-post/", AddPostView.as_view(), name="add-post"),
]
