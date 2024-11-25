from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    @property
    def total_weighted_score(self):
        active_rates = self.rates.filter(is_active=True)
        return sum(rate.score for rate in active_rates)

    @property
    def total_users_scored(self):
        return self.rates.filter(is_active=True).count()

    @property
    def average_score(self):
        if not self.total_users_scored:
            return 0
        return round(self.total_weighted_score / self.total_users_scored, 2)
