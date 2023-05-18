from functools import wraps
from inspect import stack
from time import time


class Debug:
    def __call__(self, method):
        @wraps(method)
        def inner(*args, **kwargs):
            class_name = method.__qualname__.split(".")[0]

            time_start = time()
            result = method(*args, **kwargs)
            time_end = time()
            delta = time_end - time_start
            print(f"debug --> {class_name} выполнялся {delta:.4f} ms")
            return result

        return inner
