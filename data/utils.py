import functools
import time


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        time_cost = time.time() - start_time
        print(f"{func.__name__} 耗时 {time_cost}ms")
        return result

    return clocked
