import select
import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tksctxt
import socket

g_clients = []  # List to store connected client sockets
g_client_addresses = []

def disconnectAllClients():
    # Disconnect all clients
    for client in g_clients:
        client.close()
    g_clients.clear()
    g_client_addresses.clear()
    g_app.updateConnectedClients()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # -------------------------------------------------------------------
        # row 1: connection stuff (and a clear-messages button)
        # -------------------------------------------------------------------
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
        self.ipPort.bind('<Return>', self.connectHandler)
        self.ipPort.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=5)
        padder.pack(side="left")
        #
        self.connectButton = tk.Button(self.groupCon, text='create server',
                                       command=self.connectButtonClick, width=10)
        self.connectButton.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=1)
        padder.pack(side="left")
        #
        self.clearButton = tk.Button(self.groupCon, text='clr msg',
                                     command=self.clearButtonClick)
        self.clearButton.pack(side="left")

        # -------------------------------------------------------------------
        # row 2: the message field (chat messages + status messages)
        # -------------------------------------------------------------------
        self.msgText = tksctxt.ScrolledText(height=15, width=42,
                                            state=tk.DISABLED)
        self.msgText.pack(side="top")

        # -------------------------------------------------------------------
        # row 3: sending messages
        # -------------------------------------------------------------------
        self.groupSend = tk.LabelFrame(bd=0)
        self.groupSend.pack(side="top")
        #
        self.textInLbl = tk.Label(self.groupSend, text='broadcast message')
        self.textInLbl.pack(side="left")
        #
        self.textIn = tk.Entry(self.groupSend, width=38)
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) send
        self.textIn.bind('<Return>', self.sendMessage)
        self.textIn.pack(side="left")
        #
        padder = tk.Label(self.groupSend, padx=5)
        padder.pack(side="left")
        #
        self.sendButton = tk.Button(self.groupSend, text='send to all', command=self.sendButtonClick)
        self.sendButton.pack(side="right")

        self.ClientSection = tk.LabelFrame(bd=0)
        self.ClientSection.pack(side="top")

        self.clientslabel = tk.Label(self.ClientSection, text='connected clients')
        self.clientslabel.pack(side="left")

        self.disconnectAllButton = tk.Button(self.ClientSection, text='disconnect all',
                                             command=disconnectAllClients)
        self.disconnectAllButton.pack(side='right', padx=5)  # Adjust padx as needed

        self.disconnectSelectedButton = tk.Button(self.ClientSection, text='disconnect selected',
                                                  command=lambda: self.disconnectSelectedClient(self.getSelectedIndex()))
        self.disconnectSelectedButton.pack(side='right', padx=5)  # Adjust padx as needed

        self.clientText = tksctxt.ScrolledText(self.ClientSection, height=15, width=30, state=tk.DISABLED)
        self.clientText.pack(side='top')

        self.ClientMsg = tk.LabelFrame(bd=0)
        self.ClientMsg.pack(side="top")

        self.individualmsg = tk.Label(self.ClientMsg, text='individual message')
        self.individualmsg.pack(side='left')  # Change side to 'left'

        self.sendSelectedButton = tk.Button(self.ClientMsg, text='send to selected',
                                            command=lambda: self.sendSelectedMessage(self.msgText2Text.get("1.0", tk.END)))
        self.sendSelectedButton.pack(side='right')  # Change side to 'left'

        self.msgText2Text = tk.Text(self.ClientMsg, height=15, width=30)
        self.msgText2Text.pack(side='top', anchor='w')
        # set the focus on the IP and Port text field
        self.ipPort.focus_set()

    def disconnectAllClients(self):
        # Disconnect all clients
        for client in g_clients:
            client.close()
        g_clients.clear()
        g_client_addresses.clear()
        self.updateConnectedClients()

    def disconnectSelectedClient(self, index):
        # Disconnect the selected client by index
        if 0 <= index < len(g_clients):
            client = g_clients[index]
            client.close()
            del g_clients[index]
            del g_client_addresses[index]
            self.updateConnectedClients()

    def updateConnectedClients(self):
        # Update the connected clients displayed in the GUI
        client_list = "\n".join([self.myAddrFormat(addr) for addr in g_client_addresses])
        self.clientText.configure(state=tk.NORMAL)
        self.clientText.delete(1.0, tk.END)
        self.clientText.insert(tk.END, client_list)
        self.clientText.see(tk.END)
        self.clientText.configure(state=tk.DISABLED)

    def broadcastMessage(self, message):
        # Broadcast a message to all connected clients
        for client in g_clients:
            try:
                client.sendall(message.encode('utf-8'))
            except socket.error as e:
                print(f"Error broadcasting message to client: {e}")

    def sendSelectedMessage(self, message):
        # Send a message to the selected client (assuming there is one selected)
        selected_index = self.getSelectedIndex()
        if 0 <= selected_index < len(g_clients):
            client = g_clients[selected_index]
            try:
                client.sendall(message.encode('utf-8'))
                print(f"Sent message to {self.myAddrFormat(g_client_addresses[selected_index])}: {message}")
            except socket.error as e:
                print(f"Error sending message to client: {e}")

    def getSelectedIndex(self):
        # Get the selected index in the connected clients list
        try:
            return int(self.clientText.get("sel.first", "sel.last").split('.')[0]) - 1
        except ValueError:
            return -1

    def clearButtonClick(self):
        self.msgText.configure(state=tk.NORMAL)
        self.msgText.delete(1.0, tk.END)
        self.msgText.see(tk.END)
        self.msgText.configure(state=tk.DISABLED)

    def connectButtonClick(self):
        # forward to the connect handler
        self.connectHandler()

    def sendButtonClick(self):
        # forward to the sendMessage method
        self.sendMessage()

    # the connectHandler toggles the status between connected/disconnected
    def connectHandler(self):
        if g_bConnected:
            self.disconnect()
        else:
            self.tryToConnect()

    # a utility method to print to the message field
    def printToMessages(self, message):
        self.msgText.configure(state=tk.NORMAL)
        self.msgText.insert(tk.END, message + '\n')
        # scroll to the end, so the new message is visible at the bottom
        self.msgText.see(tk.END)
        self.msgText.configure(state=tk.DISABLED)

    # if attempt to close the window, it is handled here
    def on_closing(self):
        if g_bConnected:
            if tkmsgbox.askokcancel("Quit", "You are still connected. If you quit you will be" + " disconnected."):
                self.myQuit()
        else:
            self.myQuit()

    # when quitting, do it the nice way
    def myQuit(self):
        self.disconnect()
        g_root.destroy()

    # utility address formatting
    def myAddrFormat(self, addr):
        return '{}:{}'.format(addr[0], addr[1])

    # disconnect from the server (if connected) and set the state of the program to 'disconnected'
    def disconnect(self):
        # we need to modify the following global variables
        global g_bConnected
        global g_sock

        # your code here
        if g_bConnected:
            try:
                g_sock.close()
                print("Disconnected successfully")
            finally:
                g_bConnected = False
                g_sock = None
        # once disconnected, set buttons text to 'connect'
        self.connectButton['text'] = 'connect'

    # attempt to connect to the server
    def tryToConnect(self):
        # we need to modify the following global variables
        global g_bConnected
        global g_sock

        ip_port = self.ipPort.get()
        try:
            ip, port_str = ip_port.split(':')  # Split into IP and port
            port = int(port_str)  # Convert port to an integer
        except ValueError as e:
            print(f"Invalid IP address or port format: {e}")
            return

        # Create a new socket object
        g_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Try to connect to the server using the IP and port
            g_sock.connect((ip, port))
            g_bConnected = True
            print("Connection successful.")
            self.connectButton['text'] = 'disconnect'
        except Exception as e:
            # Handle exceptions during the connection attempt
            print(f"Connection failed: {e}")
            g_bConnected = False
            self.connectButton['text'] = 'connect'

    # attempt to send the message to the server
    def sendMessage(self):
        # your code here
        # a call to g_app.textIn.get() delivers the text field's content
        # if a socket.error occurs, you may want to disconnect, in order
        # to put the program into a defined state
        message = self.textIn.get()
        try:
            g_sock.sendall(message.encode('utf-8'))
            print(f"message sent{message}")
        except socket.error as e:
            print(f"Error sending message:{e}")
            self.disconnect()


# poll messages
def pollMessages():
    # reschedule the next polling event
    global g_sock
    g_root.after(g_pollFreq, pollMessages)

    if g_sock is not None:
        try:

            rlist, _, _ = select.select([g_sock], [], [], 0.0)  # this was the issue beforehand

            if rlist:
                data = g_sock.recv(1024)
                if data:
                    print(f"Received data: {data.decode('utf-8')}")
                    # Add the received data to your message display
                    g_app.printToMessages(data.decode('utf-8'))

        except socket.error as e:
            if e.errno == socket.errno.EWOULDBLOCK:
                print("No data available")
            else:
                print(f"Socket error: {e}")


# by default, we are not connected
g_bConnected = False
g_sock = None

# set the delay between two consecutive calls to pollMessages
g_pollFreq = 200  # in milliseconds

# launch the GUI
g_root = tk.Tk()
g_app = Application(master=g_root)

# make sure everything is set to the status 'disconnected' at the beginning
g_app.disconnect()

# schedule the next call to pollMessages
g_root.after(g_pollFreq, pollMessages)

# if an attempt to close the window, handle it in the on-closing method
g_root.protocol("WM_DELETE_WINDOW", g_app.on_closing)

# start the main loop
# (which handles the GUI and will frequently call pollMessages)
g_app.mainloop()
