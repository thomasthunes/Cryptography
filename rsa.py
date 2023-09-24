import math
from sympy import isprime


def enc(x, k_pub):
    n = k_pub[0]
    e = k_pub[1]
    return (x ** e) % n


def dec(y, k_priv):
    return (y ** k_priv) % n


p, q = 11, 17
n = p * q
m = (p - 1) * (q - 1)

possible_e = []
for e in range(m - 1):
    phi = (e ** m) % n
    if phi != 1:
        continue
    if math.gcd(e, m) == 1:
        possible_e.append(e)


def find_inverse_e(n, e):
    x, y = 0, 1
    new_y = 0
    r = 1
    y_list = []
    while r != 0:
        q = n // e
        r = n % e
        new_y = x - q * y
        x = y
        y = new_y
        y_list.append(y)
        n = e
        e = r

    return get_d(y_list)


def get_d(y_list):
    if len(y_list) < 2:
        return 0
    return (y_list[-2] + n) % n


not_working = []
for e in possible_e:

    k_priv = find_inverse_e(n, e)
    k_pub = (n, e)

    y = enc(100, k_pub)
    x = dec(y, k_priv)
    # print(f'100 encrypted = {y}, y decrypted = {x}')
    if 100 == x:
        print(f'100 encrypted = {y}, y decrypted = {x}')
        print(e)
    else:
        not_working.append(e)

print(not_working)

for e in not_working:
    phi = (e ** m) % n
    if math.gcd(e, m) != 1 or phi != 1:
        print(e)

