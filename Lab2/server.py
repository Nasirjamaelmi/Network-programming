import socket

def start_server():
    # Skapa en TCP/IP-socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 60003)
    print(f"Starting up on {server_address[0]} port {server_address[1]}")
    sock.bind(server_address)

    # Lyssna efter inkommande anslutningar
    sock.listen(1)

    while True:
        # Vänta på en anslutning
        print("Waiting for a connection")
        connection, client_address = sock.accept()

        try:
            print(f"Connection from {client_address}")

            # Ta emot data i små bitar och skicka tillbaka
            while True:
                data = connection.recv(16)
                print(f"Received {data.decode()}")
                if data:
                    print("Sending data back to the client")
                    connection.sendall(data)
                else:
                    print("No data from", client_address)
                    break

        finally:
            # Stäng anslutningen
            connection.close()

if __name__ == '__main__':
    start_server()
