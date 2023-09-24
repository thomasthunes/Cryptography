g = 2
p = 11


def encrypt(x, K_pub):
    i = 5
    k_e = g ** i
    k_m = K_pub ** i
    y = x * k_m
    # print(f"transimts k_e: {k_e}, y: {y}")
    return k_e, y


def decrypt(key, d):
    y = key[1]
    k_m = key[0] ** d
    # print(f'k_m = {k_m}')
    k_m_inverse = pow(k_m, -1, p)
    # print(k_m_inverse)
    return y * k_m_inverse


d = 4
x = 5
print("original message:", x)
encrypted = encrypt(x, g ** d)
print('encrypted', encrypted[1])
decrypted = decrypt(encrypted, d)
print('decrypted', decrypted)
