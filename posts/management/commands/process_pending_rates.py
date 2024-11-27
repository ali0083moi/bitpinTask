from django.core.management.base import BaseCommand
from django.core.cache import cache
from posts.models import Rate
from django.utils import timezone
from posts.enums import RateThresholds, CacheKeys


class Command(BaseCommand):
    help = "Process pending rates based on conditions"

    def process_pending_rates(self, pending_count):
        pending_rates = Rate.objects.filter(is_pending=True, is_active=True).order_by(
            "-created_at"
        )[:pending_count]

        post_rates = {}
        for rate in pending_rates:
            if rate.post_id not in post_rates:
                post_rates[rate.post_id] = []
            post_rates[rate.post_id].append(rate)

        for _, rates in post_rates.items():
            active_rates = post.rates.filter(
                is_active=True, is_pending=False, is_valid=True
            )

            pending_avg = sum(r.score for r in rates) / len(rates)

            post = rates[0].post
            current_avg = post.average_score

            if active_rates.count() == 0:
                is_valid = True
            else:
                is_valid = (
                    abs(pending_avg - current_avg)
                    <= RateThresholds.SCORE_DEVIATION.value
                )

            Rate.objects.filter(id__in=[r.id for r in rates]).update(
                is_pending=False, is_valid=is_valid
            )

        cache.set(CacheKeys.PENDING_COUNT.value, 0)

    def handle(self, *args, **options):
        current_hour = timezone.now().hour
        pending_count = cache.get(CacheKeys.PENDING_COUNT.value) or 0

        if (
            pending_count >= RateThresholds.BATCH_SIZE.value
            or current_hour == RateThresholds.PROCESSING_HOUR.value
        ):
            print(f"Processing {pending_count} pending rates")
            self.process_pending_rates(pending_count)
        else:
            print("Conditions not met for processing pending rates")
