def setup(p, q):
    n = p * q
    m = (p - 1) * (q - 1)
    e = 3
    d = pow(e, -1, m)
    return n, e, d


def signature(x, d):
    return pow(x, d)


def verify(s, e, n):
    return pow(s, e, n)


x = 12
n, e, d = setup(3, 5)
s = signature(x, d)
x_dot = verify(s, e, n)
print(x_dot == x)
