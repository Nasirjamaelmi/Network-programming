import socket
import select

port = 60003
SockL = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SockL.bind(("", port))
SockL.listen(1)
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print(f"Local IP Address: {local_ip}")

listOfSocket = [SockL]


print("Listening on port {}" .format(port))

def brodcast(message):
    for client_socket in listOfSocket:
        if (client_socket != SockL):
            client_socket.sendall(bytearray(message, "ASCII"))


while True: 
    tup = select.select(listOfSocket, [],[])
    sock = tup[0][0]
    print(sock)

    if sock == SockL:
        sock,adress = sock.accept()
        listOfSocket.append(sock)
        sock.sendall(bytearray("{} (connected)" .format(sock.getpeername()), "utf-8"))

        brodcast("New client has joined the network")
    else:
        data = sock.recv(2048)
        if not data:
            sock.sendall(bytearray("{} (disconnected)" .format(sock.getpeername()) , "utf-8"))
            sock.close()
            listOfSocket.remove(sock)
            brodcast("Client has disconnected")
            
        else:   
            #     sock.sendall(bytearray(data, "ASCII"))
            brodcast(data.decode("ASCII"))