import math

leng= [38,45,61]
ab = [' A',' B',' C']
def SSS(a,b,c):
    return math.degrees (math.acos ((((b*b) + (c*c)) - (a*a))/(2*b*c)))
def ASA(A,b,a):
        return math.sin(math.radians(b))/math.sin(math.radians(a))*A
print(round(ASA(940,20,21),2))
for i in range(3):
    print(str(SSS(leng[(i)%3],leng[(i+1)%3],leng[(i+2)%3])) + ab[i])