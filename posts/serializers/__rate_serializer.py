from rest_framework import serializers
from ..models import Rate


class RateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["created_at"] = instance.created_at.strftime("%Y-%m-%d")
        return representation

    class Meta:
        model = Rate
        fields = ["id", "user", "post", "score", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_score(self, value):
        if not (0 <= value <= 5):
            raise serializers.ValidationError("Score must be between 0 and 5")
        return value
