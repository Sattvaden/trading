a = [1, 1]


def first(arg1):
    arg1[0] = 2
    return arg1


a = first(a)
print(a)
