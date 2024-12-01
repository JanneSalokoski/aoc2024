"""timer.py

Implement a timer decorator for measuring function runtime
"""

from time import perf_counter, perf_counter_ns


def timer(f):
    def wrap(*args, **kwargs):
        t1 = perf_counter()
        res = f(*args, **kwargs)
        t2 = perf_counter()
        print(f"Function {f.__name__!r} executed in {(t2-t1):.4f}s")

        return res

    return wrap


def timer_ns(f):
    def wrap(*args, **kwargs):
        t1 = perf_counter_ns()
        res = f(*args, **kwargs)
        t2 = perf_counter_ns()
        print(f"Function {f.__name__!r} executed in {(t2-t1)}ns")

        return res

    return wrap
