def serversideGetPlaySocket():
    

def clientnssideGetPlaySocket(host):
    pass

ans = "?"
while ans not in {"C", "S"}:
    ans = input("Do you want to be server (S) or client (S):: ")

if ans =="S":
    sock = serversideGetPlaySocket()

else:
    host = input("Enter the server's name or IP: ")
    sock = clientsideGetPlaySocket(host)    