s1 = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
]


def s_1(input):
    row = int(input[0] + input[-1], 2)
    col = int(input[1:5], 2)
    output = bin(s1[row][col])[2:].zfill(4)
    assert len(output) == 4
    return output


a = '101100'

print(2 ^ 3)

linear_count = 0
count = 0
for x in range((2 ** 6)):
    for y in range((2 ** 6)):
        count += 1
        added = x ^ y
        added = s_1(bin(added)[2:].zfill(6))
        result_x = s_1(bin(x)[2:].zfill(6))
        result_y = s_1(bin(y)[2:].zfill(6))
        if (int(result_x, 2) + int(result_y, 2)) == int(added, 2):
            print(bin(x)[2:].zfill(6), bin(y)[2:].zfill(6))
            quit()
            linear_count += 1

print(linear_count)
print(count)
