from rest_framework import generics
from ..serializers import RateSerializer
from ..models import Rate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
import redis
from django.conf import settings
from ..management.commands.process_pending_rates import Command
from ..enums import RateThresholds


class AddScoreView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            new_rate = serializer.save()

            cache_key = f"post_stats_{request.data['post']}"
            django_key = cache.make_key(cache_key)
            cached_data = cache.get(cache_key)

            redis_client = redis.StrictRedis.from_url(
                settings.CACHES["default"]["LOCATION"]
            )
            ttl = redis_client.ttl(django_key)
            if ttl < 0:  # Key doesn't exist (-2) or no expiry (-1)
                ttl = RateThresholds.TIME_TO_CACHE.value

            if cached_data:
                avg_score = float(cached_data["avg_score"])
                rate_count = int(cached_data["rate_count"])

                new_avg_score = ((avg_score * rate_count) + new_rate.score) / (
                    rate_count + 1
                )
                new_rate_count = rate_count + 1

                cache.set(
                    cache_key,
                    {"avg_score": new_avg_score, "rate_count": new_rate_count},
                    timeout=ttl,
                )

            cache_key = "is_pending_count"
            cached_data = cache.get(cache_key)
            if cached_data:
                cache.set(cache_key, cached_data + 1, timeout=None)
                if cached_data + 1 >= 500:
                    Command().process_pending_rates(cached_data + 1)
            else:
                cache.set(cache_key, 1, timeout=None)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
