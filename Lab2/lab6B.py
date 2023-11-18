import socket

def serversideGetPlaySocket(port=8080):
    Socks = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    Socks.bind(('localhost', port))
    Socks.listen(1)
    print("Waiting for a client to connect...")

    while True:
        client_socket, address = Socks.accept()
        print(f"Connected from server {address}")

        data = client_socket.recv(1024)
        print(data)
        print(data.decode("ASCII"))

        client_socket.sendall(bytearray("HTTP/1.1 200 OK\n", "ASCII"))
        client_socket.sendall(bytearray("\n", "ASCII"))
        client_socket.sendall(bytearray("<html>\n", "ASCII"))
        client_socket.sendall(bytearray("<pre>\n", "ASCII"))
        client_socket.sendall(data)
        client_socket.sendall(bytearray("\n", "ASCII"))
        client_socket.sendall(bytearray("</pre>\n", "ASCII"))
        client_socket.sendall(bytearray("</html>\n", "ASCII"))

        client_socket.close()

    # This line should not be inside the loop; it should be outside the loop
    Socks.close()

# Call the function to start the server
serversideGetPlaySocket()
