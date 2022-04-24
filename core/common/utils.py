# -*- coding: UTF-8 -*-

import functools
import time
import os

def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        time_cost = time.time() - start_time
        print(f"{func.__name__} 耗时 {time_cost}ms")
        return result

    return clocked


def mkdir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    elif not os.path.isdir(dir):
        raise (Exception(f"{dir} 不是个文件夹"))


def every(arr, fn):
    for item in arr:
        if not fn(item):
            return False
    return True
