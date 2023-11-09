def myTest():
    yield 1
    yield 5
    yield 6
    yield 99

a = myTest()
b = myTest()

print(    a.__next__()  )
print(    a.__next__()  )

print(  b.__next__()  )
print(  b.__next__()  )


print(    a.__next__()  )

#thought it was 1,2,1,2,3 but forgot that 2 is 5 and 3 = 6
#the print is 1,5,1,5,6

def FibonacciSerie(n):
    a,b = 0,1
    while(b+a < n):
        a,b = b, a+b
        yield a,b


for i in FibonacciSerie(1000000):
    print(i)