def f_addition(a, b, characteristic):
    assert len(a) == len(b)
    length = len(a)
    sum = []
    for i in range(length):
        sum_i = (a[i] + b[i]) % characteristic
        sum.append(sum_i)
    print(sum)


a = [2,0,1,3]
b = [5,2,6,1]
f_addition(a, b, 7)
