import random


def clamp(x, min, max):
    if x < min:
        return min
    elif x > max:
        return max
    return x


def lerp(a, b, amount, clamped=False):
    if clamped:
        return clamp(a + (b - a) * amount, 0, 1)
    else:
        return a + (b - 1) * amount


def map(n, a, b, c, d, clamped=False):
    if clamped:
        return clamp(lerp(c, d, (n - a) / (b - a)), c, d)
    else:
        return lerp(c, d, (n - a) / (b - a))


def randInt(a=0, b=0):
    if a < b:
        return random.randint(a, b)
    else:
        return random.randint(b, a)