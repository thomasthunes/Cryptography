import sys


# cyclic left shift on k bits
def shift(bits, k):
    return bits[k:] + bits[:k]


# logical and on two lists of bits
def AND(bits1, bits2):
    assert len(bits1) == len(bits2)
    return [b[0] * b[1] for b in zip(bits1, bits2)]


# xor on two lists of bits
def XOR(bits1, bits2):
    assert len(bits1) == len(bits2)
    return [(b[0] + b[1]) % 2 for b in zip(bits1, bits2)]


# one round of the Feistel network; returns the new left half,
# since the right half is the same as the former left half
def round(L, R, K):
    s1 = shift(L, 1)
    s2 = shift(L, 5)
    s3 = shift(L, 2)

    x1 = XOR(R, AND(s1, s2))
    x2 = XOR(x1, s3)
    x3 = XOR(x2, K)

    return x3


# derives the 4 8-bit round keys from the 32-bit key
def keySchedule(K):
    assert len(K) == 32
    return [K[off:off + 8] for off in [0, 8, 16, 24]]


# encrypts 16-bit plaintext P with 4 round keys
def encryption(P, Ks):
    # split plaintext into left and right half
    L = P[:8]
    R = P[8:]

    # repeat the same operation 4 times
    for i in range(4):
        t = L
        L = round(L, R, Ks[i])
        R = t

    # final swap
    return R + L


# encryption with 16-bit plaintext and 32-bit key
def encrypt(P, K):
    assert len(P) == 16
    assert len(K) == 32
    Ks = keySchedule(K)
    return encryption(P, Ks)


# decryption with 16-bit ciphertext and 32-bit key
def decrypt(C, K):
    assert len(C) == 16
    assert len(K) == 32
    Ks = keySchedule(K)
    Ks.reverse()
    return encryption(C, Ks)


# Converts a sequence of bytes (read from a file) into a list of bits (0s and 1s)
def bytes_to_bits(B):
    bits = []
    for i in range(len(B)):
        current_byte = B[i]
        mask = 128
        for j in range(8):
            if (current_byte >= mask):
                bits.append(1)
                current_byte -= mask
            else:
                bits.append(0)
            mask = mask // 2
    return bits


# opposite of the above operation
def bits_to_bytes(B):
    byteseq = []
    num_bytes = len(B) // 8
    assert 8 * num_bytes == len(B)
    for i in range(num_bytes):
        current_byte = 0
        bit_sequence = B[(i * 8):((i + 1) * 8)]
        mask = 128
        for j in range(8):
            current_byte += mask * int(bit_sequence[j])
            mask = mask // 2
        byteseq.append(current_byte.to_bytes(1, "big"))
    return byteseq


# writes a sequence of bytes to a file
def write_file(output_file, byteseq):
    f = open(output_file, "wb")
    for i in range(len(byteseq)):
        f.write(byteseq[i])
    f.close()


# reads a sequence of bytes from a file
def read_file(input_file):
    f = open(input_file, "rb")
    data = f.read()
    f.close()

    return data


def encrypt_plaintext(plaintext_blocks, iv, key):
    cipher_block = iv
    final_ciphertext = ""
    for block in plaintext_blocks:
        # xor the plaintext block with the cipher_block
        block = XOR(block, cipher_block)
        # encrypt the plaintext block with the key
        block = encrypt(block, key)
        # save the ciphertext as the next ciphertext block to be XORed with next block
        cipher_block = block
        # concatenate the ciphertext with the previous results
        final_ciphertext += ''.join(str(e) for e in block)

    return final_ciphertext


def main():
    if len(sys.argv) != 5:
        print("Usage: " + sys.argv[0] + " PLAINTEXT_FILE KEY_FILE IV_FILE OUTPUT_FILE")
    else:
        # extract the arguments inputted from the terminal command line
        plaintext_file = 'pad_in'  # sys.argv[1]
        key_file = 'pad_key'  # sys.argv[2]
        iv_file = 'pad_iv'  # sys.argv[3]
        output_file = 'test.txt'  # sys.argv[4]

        # # Read the plaintext, key, and IV from files and convert to bits
        plaintext = bytes_to_bits(read_file(plaintext_file))
        key = bytes_to_bits(read_file(key_file))
        iv = bytes_to_bits(read_file(iv_file))
        print(plaintext)

        # divide the input bits into equally sized lists of 16 bits
        plaintext_blocks = [plaintext[i:i + 16] for i in range(0, len(plaintext), 16)]

        # initialize the plaintext_block which will be the initialisation vector for the first iteration
        final_ciphertext = encrypt_plaintext(plaintext_blocks, iv, key)
        # convert the bitstream back to bytes, and write to the output file.
        write_file(output_file, bits_to_bytes(final_ciphertext))


main()
