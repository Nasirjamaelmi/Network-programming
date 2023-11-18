import socket

def serversideGetPlaySocket():
    Socks = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    Socks.bind(('127.0.0.1', 60003))
    Socks.listen(1)
    print("Waiting for a client to connect...")
    (sock, addr) = Socks.accept()
    return sock

def clientnssideGetPlaySocket(host):
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.connect((host, 60003))
    return sock

def winner(player1_move, player2_move):
    cond = {'R:S', 'S:P', 'P:R'}
    if (player1_move + ':' + player2_move) in cond:
        return 'win'
    elif player1_move == player2_move:
        return 'Draw'
    else:
        return 'Lose'

def play_one_round(sock):
    player1 = 0
    player2 = 0
    while player1 < 10 and player2 < 10:
        player_move = input(f"({player1}, {player2}) Choice (R,S,P): ").upper()
        sock.sendall(player_move.encode('ASCII'))
        Opposition_Move = sock.recv(1024).decode('ASCII')
        print(f"(opponent's move: {Opposition_Move})")

        result = winner(player_move, Opposition_Move)

        if result == 'win':
            player1 += 1
        elif result == 'Lose':
            player2 += 1
     

    return player1, player2

def main():
    ans = input("Do you want to be server (S) or (C): ").upper()
    while ans not in ["C", "S"]:
        ans = input("Invalid choice. Do you want to be server (S) or client (C)").upper()

    sock = None
    try:
        if ans == "S":
            sock = serversideGetPlaySocket()
        else:
            host = input("Enter the server's name or IP: ")
            sock = clientnssideGetPlaySocket(host)

        player1 = 0
        player2 = 0

        while player1 < 10 and player2 < 10:
            player1, player2 = play_one_round(sock)
            print(f"({player1}, {player2})")

        if player1 >= 10:
            print(f"Player 1 has won!")
        else:
            print(f"Player 2 has won!")

    finally:
        if sock:
            sock.close()

if __name__ == "__main__":
    main()


