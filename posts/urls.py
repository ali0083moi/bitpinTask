from django.urls import path
from .views import AddScoreView, RecievePostsView

app_name = "posts"

urlpatterns = [
    path("add-score/", AddScoreView.as_view(), name="add-score"),
    path("posts/", RecievePostsView.as_view(), name="posts-list"),
]
