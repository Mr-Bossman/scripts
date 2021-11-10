#!/bin/python
divisor = list(map(int,str(input()).split()))
dividend = [int(i)/divisor[0] for i in str(input()).split()]

for i in range((len(dividend) - len(divisor)) + 1):
    for j in range(1,len(divisor)):
        dividend[i + j] += -divisor[j] * dividend[i]

rem=1-len(divisor)
print(*dividend[:rem],",",*dividend[rem:])