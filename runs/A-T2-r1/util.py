def add(a, b):
    return a + b


def mean(xs):
    return sum(xs) / len(xs)


def clamp(x, lo, hi):
    return max(lo, min(x, hi))
