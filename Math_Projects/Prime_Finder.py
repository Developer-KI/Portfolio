def isPrime(n):
 
    # Corner case
    if n <= 1:
        print("False")
 
    # Check from 2 to n-1
    for i in range(2, n):
        if n % i == 0:
            print("False")
            break
    else:
        print("True")
