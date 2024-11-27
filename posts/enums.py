from enum import Enum


class RateLimits(Enum):
    MAXIMUM_SCORE = 5.0
    MINIMUM_SCORE = 0.0


class RateThresholds(Enum):
    SCORE_DEVIATION = 0.8
    BATCH_SIZE = 500
    PROCESSING_HOUR = 2
    TIME_TO_CACHE = 18000


class CacheKeys(Enum):
    PENDING_COUNT = "is_pending_count"
