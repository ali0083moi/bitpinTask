from rest_framework import serializers
from ..models import Post
from .rate_serializer import RateSerializer


class PostSerializer(serializers.ModelSerializer):
    average_rate = serializers.FloatField(source="average_score", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "average_rate",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
