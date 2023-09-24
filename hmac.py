import hashlib
import sys
from cipher import read_file


# writes a sequence of bytes to a file
def write_file(output_file, byteseq):
    f = open(output_file, "wb")
    f.write(byteseq)
    f.close()


def hmac_sha256(key, message):
    # block size for sha256
    block_size = 64

    # key padding
    if len(key) > block_size:
        key = hashlib.sha256(key).digest()
    if len(key) < block_size:
        key += b'\x00' * (block_size - len(key))

    # inner and outer padding
    inner_padding = bytes((x ^ 0x36) for x in key)
    outer_padding = bytes((x ^ 0x5C) for x in key)

    # hashing
    inner_hash = hashlib.sha256(inner_padding + message).digest()
    outer_hash = hashlib.sha256(outer_padding + inner_hash).digest()

    return outer_hash


def main():
    message = sys.argv[1]  # 'hash_in'
    key = sys.argv[2]  # 'hash_key'
    out = sys.argv[3]  # 'hmac_output.txt'

    # read files and calculate HMAC
    message = read_file(message)
    key = read_file(key)
    hmac = hmac_sha256(key, message)

    # write HMAC to output file
    write_file(out, hmac)


if __name__ == '__main__':
    main()