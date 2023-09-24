import assignment2_enc
import cbc


def pad_buffer1(buffer, block_size=16):
    padding_bytes = block_size - len(buffer) % block_size
    if padding_bytes == 0:
        buffer += b"\x10\x10"
    else:
        buffer += bytes([padding_bytes]) * padding_bytes
    return buffer


def pad_buffer2(buffer, block_size=16):
    padding_bytes = block_size - len(buffer) % block_size
    if padding_bytes == 0:
        buffer += b"\x10" * block_size
    else:
        buffer += bytes([padding_bytes]) * padding_bytes
    return buffer


def pad_buffer(buffer, block_size=16):
    padding_bytes = block_size - len(buffer) % block_size
    print("padding_bytes: ", padding_bytes)
    if padding_bytes == 0:
        return buffer
    else:
        padding = bytes([padding_bytes] * padding_bytes)
        return buffer + padding


def main():
    input = 'pad_in'
    iv = 'pad_iv'
    key = 'pad_key'
    out = 'enc_out.txt'

    #print("test: ", type(cbc.read_file(input)))

    buffer = pad_buffer(cbc.read_file(input))
    #print("buffer: ", buffer)
    buffer_split = cbc.splitIntoBlocks(cbc.bytes_to_bits(buffer), 16)
    #print("buffer_split: ", buffer_split)

    iv = cbc.bytes_to_bits(cbc.read_file(iv))
    k = cbc.bytes_to_bits(cbc.read_file(key))

    #print("================================================================")
    final_ciphertext = assignment2_enc.encrypt_plaintext(buffer_split, iv, k)
    final = b''
    for b in assignment2_enc.bits_to_bytes(final_ciphertext):
        final += b
    # convert the bitstream back to bytes, and write to the output file.
    print("final_ciphertext", type(final_ciphertext))
    cbc.write_file(out, assignment2_enc.bits_to_bytes(final_ciphertext))

main()

bytes_test = b'o\xa6\xaa\xc2M!\x80\x8fY\x1c\xe8'#'\x05\x05\x05\x05\x05'
print(len(bytes_test))
print(pad_buffer2(bytes_test))