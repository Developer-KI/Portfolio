s = 0
number = []


def check(n):
    global s, number
    res = 1
    number = list(map(int, str(n)))
    for c in number:
        res = res * c

    s = s + 1
    print(str(res))

    if res > 10:
        check(res)
    else:
        print("Number of steps: " + str(s))
        s = 0
