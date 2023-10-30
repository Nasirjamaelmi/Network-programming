s = "Yuji itadori"

def hello(n):
    for i in range(n):
        print(i, " Yuji itadori")
        
        
def print_all(*args):
    for arg in args:
        print(arg)
        

f = lambda a,b: a+b

def yuji():
    """ Yuji itadori """
    
a = [1,2,3,1,1,1,5,7,2]
a.sort()

stack = [ 1, 2, 3, 4 ]
stack.append(8)
stack.pop()
stack.pop()

queue = [ 1, 2, 3, 4 ]
queue.append(8)
queue.append(9)
queue.pop(0)
queue.pop(0)

a = [0,1,2,3,4,5,6,7,8,9,10]
square= []

for i in range(len(a)):
    square.append(2**i)

t = 1111, 2222, 3333

x,y,z  = t

knights = {'gallahad': 'the pure', 'robin': 'the brave'}

age = 30
if 20 <= age <= 65:
    print("vad jobbar du med")