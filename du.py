from collections import Counter
import sys

# Parse the lookup table from the input file
lookup_table = {}
with open(sys.argv[1], 'r') as f:
    for line in f:
        x, fx = line.strip().split('->')
        lookup_table[int(x, 2)] = int(fx, 2)


def xor(a, b):
    return a ^ b


def most_frequent_output_diff(output_diffs):
    """
        Returns a list containing a tuple with the most frequent element, and the frequency
        of the parameter list
    """
    return Counter(output_diffs).most_common(1)  # [0][0]


n = len(lookup_table)
d_u = []
# loop through every elem of F^n (64 elements)
for a in range(n):
    # a can not be in the zero-vectorspace
    # 0 != a ∈ (F_2^n)
    if a == 0:
        continue

    # list containing all f(x_1) + f(x_2) = b, with the current a
    output_diffs = []
    for x_1 in lookup_table.keys():
        # find x_2, we know that x_1 + x_2 equals a, thus x_1 + a equals x_2
        x_2 = xor(a, x_1)
        # find the output values of x_1 and x_2 from the lookup table, and xor them together
        # we obtain the output difference between f(x_1) and f(x_2) = b
        output_diff = xor(lookup_table[x_1], lookup_table[x_2])
        # append the output difference to the output differences table containing all
        # output differences for the current value of a
        output_diffs.append(output_diff)

    # append the  frequency of the most frequent output difference for the current a
    d_u.append(most_frequent_output_diff(output_diffs)[0][1])


# obtain differential uniformity and print it, by finding the greatest element in the d_u list
# which contains the frequency of the most frequent output differences of all choices for a
print(max(d_u))
