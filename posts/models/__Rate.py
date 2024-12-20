from django.db import models
from django.contrib.auth.models import User
from .__Post import Post
from django.db import transaction
from django.core.validators import MinValueValidator, MaxValueValidator
from ..enums import RateLimits


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="rates", db_index=True
    )
    score = models.FloatField(
        validators=[
            MinValueValidator(
                RateLimits.MINIMUM_SCORE.value, message="Score must be at least 0.0"
            ),
            MaxValueValidator(
                RateLimits.MAXIMUM_SCORE.value, message="Score cannot exceed 5.0"
            ),
        ]
    )
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pending = models.BooleanField(default=False, db_index=True)
    is_valid = models.BooleanField(default=True, db_index=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            Rate.objects.filter(
                user=self.user, post=self.post, is_active=True
            ).select_for_update().update(is_active=False)

            if not self.pk:
                self.is_pending = True

            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.post.title} - {self.score}"
