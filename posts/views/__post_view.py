from rest_framework import generics
from django.core.cache import cache
from django.db.models import Avg
from ..serializers import PostSerializer
from ..models import Post
from ..enums import RateThresholds


class RecievePostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        for post in queryset:
            cache_key = f"post_stats_{post.id}"
            stats = cache.get(cache_key)

            if stats is None:
                avg_score = post.rates.aggregate(Avg("score"))["score__avg"] or 0
                avg_score = round(float(avg_score), 2)
                rate_count = (
                    post.rates.filter(
                        is_active=True, is_valid=True, is_pending=False
                    ).count()
                    or 0
                )
                stats = {"avg_score": avg_score, "rate_count": rate_count}
                cache.set(cache_key, stats, timeout=RateThresholds.TIME_TO_CACHE.value)

            post._cached_average_score = stats["avg_score"]
            post._cached_rate_count = stats["rate_count"]

        return queryset


class RecievePostDetailView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_object(self):
        post = super().get_object()
        cache_key = f"post_stats_{post.id}"
        stats = cache.get(cache_key)

        if stats is None:
            avg_score = post.rates.aggregate(Avg("score"))["score__avg"] or 0
            avg_score = round(float(avg_score), 2)
            rate_count = (
                post.rates.filter(
                    is_active=True, is_valid=True, is_pending=False
                ).count()
                or 0
            )
            stats = {"avg_score": avg_score, "rate_count": rate_count}
            cache.set(cache_key, stats, timeout=RateThresholds.TIME_TO_CACHE.value)

        post._cached_average_score = stats["avg_score"]
        post._cached_rate_count = stats["rate_count"]
        return post


class AddPostView(generics.CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
