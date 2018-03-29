import time
from functools import wraps


class BucketLimit:
    def __init__(self, max_tokens, window_size):
        self.max_tokens = max_tokens
        self.window_size = window_size
        self.tokens = max_tokens
        self.start_time = 0


class BucketLimiter:
    def __init__(self, *limits):
        self.limits = []
        for limit in limits:
            self.limits.append(BucketLimit(limit[0], limit[1]))

    def add_limit(self, limit):
        self.limits.append(BucketLimit(limit[0], limit[1]))

    def remove_limit(self, limit):
        for_removal = None
        for each in self.limits:
            if each.max_tokens == limit[0] and each.window_size == limit[1]:
                for_removal = each
        if for_removal is not None:
            self.limits.remove(for_removal)


def bucket_limit(bucket_limiter):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            check_if_wait(bucket_limiter)
            reset_tokens(bucket_limiter)
            return_value = func(*args, **kwargs)
            reset_time_and_decrement(bucket_limiter)
            return return_value

        return wrapper

    return decorator


def check_if_wait(bucket_limiter):
    for limit in bucket_limiter.limits:
        if limit.tokens == 0:
            delta = time.time() - limit.start_time
            sleep_time = limit.window_size - delta
            if sleep_time > 0:
                time.sleep(sleep_time)


def reset_tokens(bucket_limiter):
    for limit in bucket_limiter.limits:
        delta = time.time() - limit.start_time
        if delta >= limit.window_size:
            limit.tokens = limit.max_tokens


def reset_time_and_decrement(bucket_limiter):
    for limit in bucket_limiter.limits:
        if limit.tokens == limit.max_tokens:
            limit.start_time = time.time()
        limit.tokens = limit.tokens - 1
