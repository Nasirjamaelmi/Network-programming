
import select
import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tksctxt
import socket
import threading

selected_clients = set()
client_sockets = []

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
    
        #-------------------------------------------------------------------
        # row 1: connection stuff (and a clear-messages button)
        #-------------------------------------------------------------------
        self.groupCon = tk.LabelFrame(bd=0)
        self.groupCon.pack(side="top")
        #
        self.ipPortLbl = tk.Label(self.groupCon, text='IP:port', padx=10)
        self.ipPortLbl.pack(side="left")
        #
        self.ipPort = tk.Entry(self.groupCon, width=20)
        self.ipPort.insert(tk.END, 'localhost:60003')
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) connect
        self.ipPort.bind('<Return>', connectHandler)
        self.ipPort.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=5)
        padder.pack(side="left")
        #
        self.connectButton = tk.Button(self.groupCon,text='Create server',
            command = connectButtonClick, width=10)
        self.connectButton.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=1)
        padder.pack(side="left")
        #
        self.clearButton = tk.Button(self.groupCon, text='clr msg',
            command = clearButtonClick)
        self.clearButton.pack(side="left")

        
        #-------------------------------------------------------------------
        # row 2: the message field (chat messages + status messages)
        #-------------------------------------------------------------------
        self.msgText = tksctxt.ScrolledText(height=15, width=42,
            state=tk.DISABLED)
        self.msgText.pack(side="top")

        
        #-------------------------------------------------------------------
        # row 3: sending messages
        #-------------------------------------------------------------------
        self.groupSend = tk.LabelFrame(bd=0)
        self.groupSend.pack(side="top")
        #
        self.textInLbl = tk.Label(self.groupSend, text='brodcast message')
        self.textInLbl.pack(side="left")
        #
        self.textIn = tk.Entry(self.groupSend, width=38)
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) send
        self.textIn.bind('<Return>', broadcast_to_all_clients_and_server)
        self.textIn.pack(side="left")
        #
        padder = tk.Label(self.groupSend, padx=5)
        padder.pack(side="left")
        #
        self.sendButton = tk.Button(self.groupSend, text = 'send to all',
            command = send_to_all_clients_and_server)
        self.sendButton.pack(side="right")
        
        self.ClientSection = tk.LabelFrame(bd=0)
        self.ClientSection.pack(side="top")

        self.clientslabel = tk.Label(self.ClientSection, text='connected clients')
        self.clientslabel.pack(side="left")

        self.disconnectAllButton = tk.Button(self.ClientSection, text='disconnect all', command=disconnect_selected_clients)
        self.disconnectAllButton.pack(side='right', padx=5)  # Adjust padx as needed
  

        self.disconnectSelectedButton = tk.Button(self.ClientSection, text='disconnect selected', command=disconnect_selected_clients)
        self.disconnectSelectedButton.pack(side='right', padx=5)  # Adjust padx as needed
        
     
        self.clientText = tksctxt.ScrolledText(self.ClientSection,height=15, width=30, state=tk.DISABLED)
        self.clientText.pack(side='top')

       

        self.ClientMsg = tk.LabelFrame(bd=0)
        self.ClientMsg.pack(side="top")

        self.indivudualmsg = tk.Label(self.ClientMsg, text='indidvidual message')
        self.indivudualmsg.pack(side ='left')  # Change side to 'left'
        
        self.sendSelectedButton = tk.Button(self.ClientMsg, text='send to selected')
        self.sendSelectedButton.pack(side='right')  # Change side to 'left'
        
        self.msgText2Text = tk.Text(self.ClientMsg, height=15, width=30)
        self.msgText2Text.pack(side='top', anchor='w')
        
        
        
        # set the focus on the IP and Port text field
        self.ipPort.focus_set()

def clearButtonClick():
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.delete(1.0, tk.END)
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

def connectButtonClick():
    # forward to the connect handler
    connectHandler(g_app)

def sendButtonClick():
    # forward to the sendMessage method
    sendMessage(g_app)

# the connectHandler toggles the status between connected/disconnected
def connectHandler(master):
    if g_bConnected:
        disconnect()
    else:
        tryToConnect()

# a utility method to print to the message field        
def printToMessages(message):
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.insert(tk.END, message + '\n')
    # scroll to the end, so the new message is visible at the bottom
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

# if attempt to close the window, it is handled here
def on_closing():
    if g_bConnected:
        if tkmsgbox.askokcancel("Quit",
            "You are still connected. If you quit you will be"
            + " disconnected."):
            myQuit()
    else:
        myQuit()

# when quitting, do it the nice way    
def myQuit():
    disconnect()
    g_root.destroy()

# utility address formatting
def myAddrFormat(addr):
    return '{}:{}'.format(addr[0], addr[1])

def broadcast_to_all_clients(message):
    global g_sock
    for client_sock in client_sockets:
        try:
            client_sock.sendall(message.encode('utf-8'))
            printToMessages(f"Broadcast to {myAddrFormat(client_sock.getpeername())}: {message}")
        except socket.error as e:
            print(f"Error broadcasting message to {myAddrFormat(client_sock.getpeername())}: {e}")

# disconnect from server (if connected) and
# set the state of the programm to 'disconnected'
def disconnect():
    # we need to modify the following global variables
    global g_bConnected
    global g_sock

    # your code here
    if g_bConnected:
        try:
            g_sock.close()
            broadcast("Disconnected successfully")
        finally:
            g_bConnected = False
            g_sock = None
    # once disconnected, set buttons text to 'Create server'
    g_app.connectButton['text'] = 'Create server'

def myAddrFormat(addr):
    return '{}:{}'.format(addr[0], addr[1])
   
# attempt to connect to server    
def tryToConnect():
    global g_bConnected
    global g_sock

    if not g_bConnected:
        try:
            ip_port = g_app.ipPort.get()
            ip, port_str = ip_port.split(':')  # Split into IP and port
            port = int(port_str)  # Convert port to an integer

            # Create a new socket object
            g_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Bind the socket to the specified IP and port
            g_sock.bind((ip, port))
            g_sock.listen(5)  # Listen for incoming connections

            g_bConnected = True
            broadcast(f"Server created and listening on {ip}:{port}")
            g_app.connectButton['text'] = 'Disconnect'

            # Start a new thread to handle client connections
            threading.Thread(target=accept_clients).start()

        except Exception as e:
            # Handle exceptions during server creation
            broadcast(f"Server creation failed: {e}")
            g_bConnected = False
            g_app.connectButton['text'] = 'Create server'

    # try to connect to the IP address and port number
    # as indicated by the text field g_app.ipPort
    # a call to g_app.ipPort.get() delivers the text field's content
    # if connection successful, set the program's state to 'connected'
    # (e.g. g_app.connectButton['text'] = 'disconnect' etc.)
def accept_clients():
    global g_bConnected
    global g_sock

    # Accept clients in a loop
    while g_bConnected:
        client_sock = None  # Initialize client_sock outside the try block
        try:
            client_sock, client_addr = g_sock.accept()
            print(f"Accepted connection from {myAddrFormat(client_addr)}")
            printToClients(f"Connected to {myAddrFormat(client_addr)}")

            # You can handle the client connection in a separate thread or function
            # For simplicity, I'm printing the client address here
            print(f"Connected to {myAddrFormat(client_addr)}")
        except socket.error as e:
            if g_bConnected:
                print(f"Error accepting client: {e}")
            else:
                # g_bConnected is False, so the server is no longer accepting clients
                break
        finally:
            if client_sock:
                try:
                    client_sock.close()  # Make sure to close the client socket if it was created
                except Exception as close_error:
                    print(f"Error closing client socket: {close_error}")


        
def printToClients(message):
    g_app.clientText.configure(state=tk.NORMAL)

    # Insert the message with a tag for the client address
    g_app.clientText.insert(tk.END, message + '\n', 'client_tag')

    # Add a tag for the newly inserted client address
    g_app.clientText.tag_add('client_tag', tk.END + '-2l', tk.END)

    # Bind a function to handle clicks on client addresses
    g_app.clientText.tag_bind('client_tag', '<Button-1>', lambda event: handle_client_click(event))

    g_app.clientText.see(tk.END)
    g_app.clientText.configure(state=tk.DISABLED)
    
def handle_client_click(event):
    # Get the index of the clicked character
    index = g_app.clientText.index(tk.CURRENT)

    # Extract the client address from the clicked line
    clicked_line = g_app.clientText.get(index + ' linestart', index + ' lineend')
    client_address = tuple(map(str, clicked_line.strip().split(':')))
    broadcast(f"Clicked on client: {client_address}")

    # Update the selected clients
    select_client(client_address)

def disconnect_client(client_address):
    # Implement disconnect logic here
   broadcast(f"Disconnecting client: {client_address}")

def select_client(client_address):
    # Implement select logic here
    broadcast(f"Selecting client: {client_address}")
    selected_clients.add(client_address)

def disconnect_selected_clients():
    global g_bConnected
    global g_sock

    # Disconnect the selected clients
    for client_address in selected_clients.copy():
        disconnect_client(client_address)



# attempt to send the message (in the text field g_app.textIn) to the server
def sendMessage(master):
    global g_sock
    # your code here
    # a call to g_app.textIn.get() delivers the text field's content
    # if a socket.error occurrs, you may want to disconnect, in order
    # to put the program into a defined state
    message = g_app.textIn.get()
    try: 
        g_sock.sendall(message.encode('utf-8'))
        print(f"message sent{message}")
        broadcast_to_all_clients(message)
    except socket.error as e:
        print(f"Error sending message:{e}")
        disconnect()


# poll messages
def pollMessages():
    # reschedule the next polling event
    global g_sock
    g_root.after(g_pollFreq, pollMessages)

    if g_sock is not None:
        try:
          
            rlist, _, _ = select.select([g_sock], [], [], 0.0)  #this was the issue beforehand

            if rlist:
                data = g_sock.recv(1024)
                if data:
                    broadcast(f"Received data: {data.decode('utf-8')}")
                    # Add the received data to your message display
                    printToMessages(data.decode('utf-8'))

        except socket.error as e:
            if e.errno == socket.errno.EWOULDBLOCK:
               broadcast("No data available")
            else:
                broadcast(f"Socket error: {e}")

        
      
    # your code here
    # use the recv() function in non-blocking mode
    # catch a socket.error exception, indicating that no data is available


def broadcast_to_all_clients_and_server(message):
    global g_sock
    for client_sock in client_sockets:
        try:
            client_sock.sendall(message.encode('utf-8'))
            printToMessages(f"Broadcast to {myAddrFormat(client_sock.getpeername())}: {message}")
        except socket.error as e:
            print(f"Error broadcasting message to {myAddrFormat(client_sock.getpeername())}: {e}")
    
    # Display the broadcast message in the server's message text field
    printToMessages(f"Broadcast to all: {message}")
    
def broadcast(message):
    # Broadcast to all connected clients and display in the server's message text field
    broadcast_to_all_clients_and_server(message)

def send_to_all_clients_and_server():
    global g_sock

    # Get the message from the textIn field
    message = g_app.textIn.get()

    # Broadcast the message to all connected clients
    for client_sock in client_sockets:
        try:
            client_sock.sendall(message.encode('utf-8'))
            printToMessages(f"Broadcast to {myAddrFormat(client_sock.getpeername())}: {message}")
        except socket.error as e:
            print(f"Error broadcasting message to {myAddrFormat(client_sock.getpeername())}: {e}")

    # Display the broadcast message in the server's message text field
    printToMessages(f"Broadcast to all: {message}")

    # Print the message to every client
    for client_sock in client_sockets:
        try:
            client_sock.sendall(message.encode('utf-8'))
        except socket.error as e:
            print(f"Error sending message to {myAddrFormat(client_sock.getpeername())}: {e}")

    # Clear the textIn field after sending the message
    g_app.textIn.delete(0, tk.END)




# by default we are not connected
g_bConnected = False
g_sock = None

# set the delay between two consecutive calls to pollMessages
g_pollFreq = 200 # in milliseconds

# launch the gui
g_root = tk.Tk()
g_app = Application(master=g_root)

# make sure everything is set to the status 'disconnected' at the beginning
disconnect()

# schedule the next call to pollMessages
g_root.after(g_pollFreq, pollMessages)

# if attempt to close the window, handle it in the on-closing method
g_root.protocol("WM_DELETE_WINDOW", on_closing)

# start the main loop
# (which handles the gui and will frequently call pollMessages)
g_app.mainloop()
