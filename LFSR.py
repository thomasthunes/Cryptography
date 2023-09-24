eirik = 10000000000000000000000000000110000110011111110000110010011100101111110000110111011001011011001110110011111010100000011001011101000001011100111010001101011110110110010001110000100010100100011101101111000011000010101101110010001011101001100110100011101000001011011000000101010111110001100110000101101100111000010111011101001001000100010101011001110011000000011111100100010111101000100110010010010111001011000001110001001000000111011001110110110000111000111101001010011110010110000000010000000101110111


def xor(a, b):
    """
    XOR operation between two bits
    """
    return a ^ b


def polynomial(state, polynomial):
    """
    Method for extracting the bits in the state that should be XORed with each other.\n
    saves the first index as current bit, then XORs the current bit with the next bit in the polynomial, which is saved
    and XORed with the next bit in the polynomial.
    :param state:
    :param polynomial:
    :return: The result of all xor operations
    """
    current_bit = state[polynomial[0]]
    # Begins at the second bit of the polynomial, as the first is already saved in "current bit"
    i = 1
    while i < len(polynomial):
        current_bit = xor(current_bit, state[polynomial[i]])
        i += 1
    return current_bit


def lfsr(state, polynomial_indices):
    """
    Method for creating a sequence of the least significant bits after 500 iterations of the LFSR algorithm.
    Starts at state = 100000000000000000000000000001, and then saves the least significant bit (the last bit in the
    state), before it finds the new bit to be inserted at the beginning of the state, by XORing the bits in the
    positions of the given polynomial.
    :param state:
    :param polynomial_indices:
    :return:
    """
    seq = ""
    # loop until the output sequence has length 500
    while len(seq) < 500:
        # compute the next bit of the LFSR using the feedback polynomial
        new_bit = polynomial(state, polynomial_indices)
        # append the outgoing bit to the output sequence
        seq += str(state[-1])
        # shift the state to the right by one bit
        state = state[:-1]
        # insert the new bit into the first position of the state
        state.insert(0, new_bit)

    with open('lfsr_output.txt', 'w') as f:
        f.write(seq)
    return seq


# The primitive polynomial used to compute the LFSR
# x^30 + x^24 + x^20 + x^16 + x^14 + x^13 + x^11 + x^7 + x^2 + x^1 + 1
# (source: https://www.partow.net/programming/polynomials/index.html#deg03)
feedback_polynomial = [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1]

# creates a list containing the indexes of the bits that should be XORed in each iteration of the lfsr() method
xor_indices = []
for i in range(len(feedback_polynomial)):
    if feedback_polynomial[i] == 1:
        xor_indices.append(i)

# Initialize the LFSR state as a list of 30 bits, with the first and last bits set to 1
state = [0] * 30
state[0] = 1
state[29] = 1

result = lfsr(state, xor_indices)

signals = {
    "red": "-",
    "blue": "--",
    "green": "---",
    "yellow": "----"
}

print(signals["red"])
