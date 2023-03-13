import math

n = 1


def solve():
    global n
    angle = 360 / n
    
    res = 1 * 1 * math.sin(angle * (math.pi / 180))

    print("Area is: " + str(res/2 * n) + " " + str(n))
    
    if float(res/2 * n) >= 3.14:
        print("Estimated at 99% at: " + str(n))
    else:
        n = n + 1
        solve()
        
    

