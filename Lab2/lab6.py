import socket

def serversideGetPlaySocket(port = 8080):
    Socks = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    Socks.bind(('localhost', port))
    Socks.listen(1)
    print("Waiting for a client to connect...")
    
    try:
        while True:
            client_socket, address = Socks.accept()
            print("Connect form server {address}")


            data = client_socket.recv(1024)
            print("Request accpeted")
            print(data.decode("ASCII"))
            client_socket.close()

    finally:
        Socks.close()
serversideGetPlaySocket()

