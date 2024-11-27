from rest_framework import generics
from ..serializers import PostSerializer
from ..models import Post


class RecievePostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class RecievePostDetailView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
