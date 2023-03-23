import math

step = 3
Pi_c = 3
Pi_p = 0


def calculate(n):
    global Pi_c, Pi_p
    Pi_p = Pi_c
    Pi_c = (n * (math.sin(math.radians(180) - math.radians((((n - 2) * 180) / n))) / math.sin(math.radians(((n - 2) * 180) / (n * 2))))) / 2

    print(str(Pi_c))

calculate(1000000000)
print(math.pi)
