def add(a, b):
    """두 값을 더해서 돌려준다."""
    return a + b


def mean(xs):
    """숫자 목록의 평균을 돌려준다. 목록이 비어 있으면 ZeroDivisionError가 난다."""
    return sum(xs) / len(xs)


def clamp(x, lo, hi):
    """x를 lo 이상 hi 이하 범위 안으로 맞춰서 돌려준다."""
    return max(lo, min(x, hi))
