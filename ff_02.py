def add(x, k):
    return x ^ k


# Multiplies two numbers in the finite field GF(2^6) with the primitive polynomial x^6 + x + 1.
def multiply(a: int, b: int) -> int:
    # Define the primitive polynomial
    p = 0b1000011  # x^6 + x + 1 in binary
    # Initialize the result to zero
    result = 0
    # Perform the multiplication in the field
    while a > 0:
        # If the least significant bit of a is 1, add b to the result
        if a & 1:
            result ^= b
        # Shift b to the left by one bit
        b <<= 1
        # Reduce b modulo the primitive polynomial if it overflows
        if b & 0b1000000:  # 0b1000:
            b ^= p
        # Shift a to the right by one bit
        a >>= 1
    return result


# calculate F(x, k) = x^3 + (x+k)^3 + k
def ff(x, k):
    x2 = multiply(x, x)
    x3 = multiply(x2, x)
    xk = add(x, k)
    xk2 = multiply(xk, xk)
    xk3 = multiply(xk2, xk)
    return x3 ^ xk3 ^ k


n = 6
count = 0
file = open("finite_field_lookupTable_6bit.txt", "w")
for x in range(2 ** n):
    for k in range(2 ** n):
        count += 1
        file.write(f"{bin(x)[2:].zfill(n)},{bin(k)[2:].zfill(n)}->{bin(ff(x, k))[2:].zfill(n)}\n")
print(count)
