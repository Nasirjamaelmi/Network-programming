import socket



def serversideGetPlaySocket():
    Socks = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    Socks.bind(('127.0.0.1', 60003))
    Socks.listen(1)
    
    while True:
        print('\nlistening...\n')
        (SockC, addr) = Socks.accept()
        print('connection from {}' . format(addr))
        while True:
            data = SockC.recv(1024)
            if not data:
                break
            print('recived:', data.decode('ascii'))
            answer = 'thanks for the data!'
            SockC.sendall( bytearray(answer,'ascii'))
            print('answered:', answer)
        SockC.close()
        print('client {} disconnected'.format(addr))
        
        
def clientnssideGetPlaySocket(host):
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 60003))
    message = input('type your message:')
    sock.sendall(bytearray(message,'ascii'))
    print('sent:', message)
    
    data = sock.recv(1024)
    print('recived:', data.decode('ascii'))
    sock.close()

def playgame(sock):
    player1 = 0
    player2 = 0
    ans = "?"
    while ans is not {"R","S","P"}:
        ans = input("Invalid choice: R,S,P").upper
    return ans
          

ans = "?"
while ans not in {"C", "S"}:
    ans = input("Do you want to be server (S) or client (C):: ")

if ans =="S":
    sock = serversideGetPlaySocket()
    

else:
    host = input("Enter the server's name or IP: ")
    sock = clientnssideGetPlaySocket(host)