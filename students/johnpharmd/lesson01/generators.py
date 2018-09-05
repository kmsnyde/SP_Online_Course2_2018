#!/usr/bin/env python


def intsum():
    """
    Adds next integer y to integer value store x
    """
    x = 0
    y = 0
    while True:
        x += y
        y += 1
        yield x


def doubler():
    """
    Doubles the value of x
    """
    x = 1
    while True:
        yield x
        x *= 2


def fib():
    """
    Fibonacci seq generator
    """
    i = 1
    x = 1
    flist = [1, 1]
    while True:
        yield x
        i += 1
        if i == 2:
            x = 1
        else:
            x = flist[i-2] + flist[i-1]
        flist.append(x)


def prime():
    """
    Correctly generates sequence of only prime numbers through 113.
    """
    i = 2
    while True:
        if i in (2, 3, 5, 7):
            yield i
        elif i % 2 == 1 and i % 3 != 0 and i % 5 != 0 and i % 7 != 0:
            yield i
        i += 1
