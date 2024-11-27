from rest_framework import generics
from django.core.cache import cache
from django.db.models import Avg
from ..serializers import PostSerializer
from ..models import Post


class RecievePostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        for post in queryset:
            cache_key = f"post_avg_score_{post.id}"
            avg_score = cache.get(cache_key)

            if avg_score is None:
                avg_score = post.rates.aggregate(Avg("score"))["score__avg"] or 0
                avg_score = round(float(avg_score), 2)
                cache.set(cache_key, avg_score, timeout=15)

            post._cached_average_score = avg_score

        return queryset


class RecievePostDetailView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_object(self):
        post = super().get_object()
        cache_key = f"post_avg_score_{post.id}"
        avg_score = cache.get(cache_key)

        if avg_score is None:
            avg_score = post.rates.aggregate(Avg("score"))["score__avg"] or 0
            avg_score = round(float(avg_score), 2)
            cache.set(cache_key, avg_score, timeout=15)

        post._cached_average_score = avg_score
        return post
