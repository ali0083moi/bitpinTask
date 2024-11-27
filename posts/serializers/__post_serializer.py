from rest_framework import serializers
from ..models import Post
from .__rate_serializer import RateSerializer


class PostSerializer(serializers.ModelSerializer):
    average_rate = serializers.FloatField(source="average_score", read_only=True)
    user_rate = serializers.SerializerMethodField()

    def get_user_rate(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            rate = obj.rates.filter(user=request.user, is_active=True).first()
            return rate.score if rate else None
        return None

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "average_rate",
            "user_rate",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]