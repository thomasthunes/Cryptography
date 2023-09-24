import sys
import time
from random import randint
from math import gcd
from hashlib import sha256


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read().split()


def write_file(filename, data):
    with open(filename, 'w') as f:
        f.write('\n'.join(map(str, data)))


def generate_k(p):
    """
        generates an ephemeral key that satisfies the criterias:\n
            - K_e ∈ {1, 2, . . . , p - 2}
            -  gcd(K_e, p - 1) = 1
    """
    # initialize k
    k = 0
    # picks a random number in the discrete interval [1, p-2] and continues to
    # try different values until the second criteria is satisfied
    while gcd(k, p - 1) != 1:
        k = randint(1, p - 2)
    return k


def elgamal():
    # read contents of files given as arguments in the launch command
    # parameters, private key and message
    params = read_file(sys.argv[1])
    d = int(read_file(sys.argv[2])[0])
    msg = int(read_file(sys.argv[3])[0])
    output_file = sys.argv[4]
    # save parameters (public key)
    p, g, b = int(params[0]), int(params[1]), int(params[2])
    # generate the ephemeral key 
    k = generate_k(p)
    # find r with the formula ((g^k) % p)
    r = pow(g, k, p)
    # find the inverse of the ephemeral key
    k_inverse = pow(k, -1, p - 1)
    # calculate s using the formula
    # s = ((x - dr) * k^-1 ) % p-1
    s = ((msg - (d * r)) * k_inverse) % (p - 1)

    write_file(output_file, [r, int(s)])


elgamal()
