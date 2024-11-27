from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_weighted_score(self):
        active_rates = self.rates.filter(
            is_active=True, is_pending=False, is_valid=True
        )
        return sum(rate.score for rate in active_rates)

    @property
    def total_users_scored(self):
        return self.rates.filter(
            is_active=True, is_pending=False, is_valid=True
        ).count()

    @property
    def average_score(self):
        active_rates = self.rates.filter(
            is_active=True, is_pending=False, is_valid=True
        )
        if not active_rates.exists():
            return 0
        avg_rate = active_rates.aggregate(avg_score=models.Avg("score"))["avg_score"]
        return round(float(avg_rate), 2)

    def __str__(self):
        return f"{self.title} - {self.author.username}"
