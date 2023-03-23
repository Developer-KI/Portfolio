x = 0
y = 0
z = 0

a = 0
b = 0
c = 0

while True:
    x = x + 1
    y = x / 2

    a = 2 * y
    b = y * y - 1
    c = y * y + 1
    formula = a, b, c

    if a == round(a) and b == round(b) and c == round(c) and a + b > c:
        z = z + 1
        print(z)
        print(formula)

    if x/2 == 100:
        break

print("\nStopped generating Pythagorean triplets.")
