
def get_file_content(file_name, n_split):
    """
        Reads the content of a file and splits it into two parts if it's the plaintext
        and 4 parts if it's the key
    """
    with open(file_name, "r") as input_file:
        data = input_file.read().splitlines()[0]

    split_size = len(data) // n_split
    min, max = 0, split_size

    splits = []
    # adds 8 first bits to list, and then the 8 next bits
    for i in range(n_split):
        chunk = data[min:max]
        splits.append(chunk)
        min += split_size
        max += split_size
    return splits


def toCharArray(bit_stream):
    """
    converts string to char array
    :param bit_stream:
    :return: bit_array
    """
    bit_array = []
    for char in bit_stream:
        bit_array.append(char)
    return bit_array


def shift_left(bit_stream, k):
    """
        shifts the bits left by k
    """
    bit_stream = bin(bit_stream)[2:].zfill(8)
    bit_array = toCharArray(bit_stream)
    l = len(bit_array)
    new_bit_array = [0] * 8
    for i in range(l):
        new_index = (i - k) % l
        new_bit_array[new_index] = bit_array[i]

    return int(''.join(str(elem) for elem in new_bit_array), 2)


def decrypt(L, R, K, current_iteration=3):
    """
        decrypts the ciphertext using the given key and returns the plaintext,
        works simular to the encryption method, but the operations are done in
        the opposite order
    """
    if current_iteration < 0:
        result = bin(L)[2:].zfill(8) + bin(R)[2:].zfill(8)
        return result
    # If first iteration, swap happens two times == zero times
    if current_iteration != 3:
        L, R = R, L

    R = ((shift_left(L, 2) ^ R) ^ K[current_iteration])
    R = ((shift_left(L, 1) & shift_left(L, 5)) ^ R)
    current_iteration -= 1
    result = decrypt(L, R, K, current_iteration)
    return result


def encrypt(L, R, K, current_iteration=0):
    """
        A recursive method that encrypts the ciphertext using the given key with four iterations \n
        returns the result after number of rounds exceeds the maximum number of iterations
    """
    n_rounds = 4
    if current_iteration == n_rounds:
        L, R = R, L
        result = bin(L)[2:].zfill(8) + bin(R)[2:].zfill(8)
        return result

    R = ((shift_left(L, 1) & shift_left(L, 5)) ^ R)
    R = ((shift_left(L, 2) ^ R) ^ K[current_iteration])
    L, R = R, L
    current_iteration += 1
    result = encrypt(L, R, K, current_iteration)
    return result


def main(input_file, key_file="cipher_key.txt", type_of_operation="encrypt"):
    """
        Main method performing simple reformatting and variable instantiations.\n
        :return the ciphertext or the plaintext, depending on the type_of_operation parameter
    """
    inn = get_file_content(input_file, 2)
    K = get_file_content(key_file, 4)

    L, R = int(inn[0], 2), int(inn[1], 2)
    K = [int(K[0], 2), int(K[1], 2), int(K[2], 2), int(K[3], 2)]
    if type_of_operation == "encrypt":
        t1 = encrypt(L, R, K, current_iteration=0)
    else:
        t1 = decrypt(L, R, K, current_iteration=3)
    return t1


print("encrypt1")
expected = str(1100001011101010)
encrypt1 = main("cipher_in1.txt")
f = open('in1_encrypted.txt', 'w')
f.write(encrypt1)
print(f"{encrypt1}  ==  {expected}")
print(encrypt1 == expected)
print("------------------------------------------------------")

print("encrypt2")
expected = str(1001001100111111)
encrypt2 = main("cipher_in2.txt")
f = open('in2_encrypted.txt', 'w')
f.write(encrypt2)
print(f"{encrypt2}  ==  {expected}")
print(encrypt2 == expected)
print("------------------------------------------------------")

print("decrypt1:")
expected = str(1011001111110000)
decrypt1 = main("cipher_out1.txt", type_of_operation="decrypt")
f = open('out1_decrypted.txt', 'w')
f.write(decrypt1)
print(f"{decrypt1}  ==  {expected}")
print(decrypt1 == expected)
print("------------------------------------------------------")

print("decrypt2:")
expected = str(1011001000111010)
decrypt2 = main("cipher_out2.txt", type_of_operation="decrypt")
f = open('out2_decrypted.txt', 'w')
f.write(decrypt2)
print(f"{decrypt2}  ==  {expected}")
print(decrypt2 == expected)
print("------------------------------------------------------")
