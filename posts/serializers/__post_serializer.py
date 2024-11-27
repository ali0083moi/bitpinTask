from rest_framework import serializers
from ..models import Post
from .__rate_serializer import RateSerializer


class PostSerializer(serializers.ModelSerializer):
    average_rate = serializers.SerializerMethodField()
    user_rate = serializers.SerializerMethodField()
    user_rate_count = serializers.SerializerMethodField()

    def get_average_rate(self, obj):
        return getattr(obj, "_cached_average_score", obj.average_score)

    def get_user_rate(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            rate = obj.rates.filter(user=request.user, is_active=True).first()
            return rate.score if rate else None
        return None

    def get_user_rate_count(self, obj):
        return obj.rates.filter(is_active=True).count() or 0

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "average_rate",
            "user_rate",
            "user_rate_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
