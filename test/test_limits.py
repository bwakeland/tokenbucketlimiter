import time

from bucketlimiter import BucketLimiter
from bucketlimiter import bucket_limit


def test_bucket_limiter():
    test_limits = BucketLimiter((2, 1))

    @bucket_limit(test_limits)
    def limited_function():
        return 2

    cur_time = time.time()

    for i in range(3):
        x = limited_function()

    assert ((time.time() - cur_time) >= 1)
    assert (x == 2)


def test_double_bucket_limiter():
    test_limits = BucketLimiter((3, 1))
    global_limits = BucketLimiter((2, 1))

    @bucket_limit(test_limits)
    @bucket_limit(global_limits)
    def limited_function():
        return 2

    cur_time = time.time()

    for i in range(3):
        x = limited_function()

    assert ((time.time() - cur_time) >= 1)
    assert (x == 2)

def test_add_remove():
    test_limits = BucketLimiter((2, 1))

    @bucket_limit(test_limits)
    def limited_function():
        return 2


    test_limits.remove_limit((2, 1))
    cur_time = time.time()
    for i in range(3):
        x = limited_function()

    assert((time.time() - cur_time) < 1)
    assert(x == 2)

    test_limits.add_limit((5, 1))
    cur_time = time.time()

    for i in range(6):
        x = limited_function()

    assert ((time.time() - cur_time) >= 1)
    assert (x == 2)

