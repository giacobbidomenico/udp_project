import socket as sk
import os
import threading
import random

BUFFER_SIZE = 4096
STATE_FILE = "temp.txt"
mutex = threading.Lock()

#class that manages the server logic
class ModelServer:

    #initialization of the UDP socket through which 
    #client requests are received
    def __init__(self):
        self.sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        self.port_listening = {}
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
        
    
    #class communications are written to a file using this 
    #method, because the view is blocked by the mainloop method
    def write_state_on_file(self, message):
        try:
            with open(STATE_FILE, "a") as f:
                f.write("\n" + message)
                f.close()
        except:
            f.write("Wait")
    
    #method that sets the main socket, the one that receives 
    #commands from clients and associates parallel threads by port number
    #for their management
    def set_server_address(self, address, port):
        return self.set_address(self.sock, (address, port))

    #method that associates the socket, passed as a parameter, the ip address 
    #and port number of the client with which it will have to communicate        
    def set_address(self, new_socket, address):
        try:
            new_socket.bind(address)
        except:
            return False
        return True

    #method that takes care of receiving requests from clients, 
    #assigning each processing to a thread with a reserved socket on another port
    def handle(self, view):

        while True:
            print("server wait a client")
            #find a port that is not already reserved
            while True:
                port_server_for_client = random.randint(0, 65535)
                if not self.port_listening.get(port_server_for_client):
                    self.port_listening[len] = port_server_for_client
                    break
 
            #receives a request from a client
            commands, address_client = self.sock.recvfrom(BUFFER_SIZE)
            commands = commands.decode("utf8").split()
            real_address_client, real_port = address_client
            
            #execute the request on another thread
            new_socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
            self.set_address(new_socket, (real_address_client, port_server_for_client))
            thread = threading.Thread(target = self.handle_command, args=(commands, 
                                                                          new_socket,
                                                                          address_client))
            
            #thread stops when main thread dies
            thread.daemon = True
            thread.start()

    #method that detects commands sent by clients and processes responses
    #to received commands
    def handle_command(self, commands, new_socket, address_client):
        print(commands)
        
        if commands[0] == "check":
            #manage parallel access to the following piece of code
            mutex.acquire()
            new_socket.sendto("ok".encode(), address_client)
        if commands[0] == "list":
            #manage parallel access to the following piece of code
            mutex.acquire()
            self.handle_list(new_socket, address_client)
        if commands[0] == "get":
            #manage parallel access to the following piece of code
            mutex.acquire()
            self.handle_get(commands, new_socket, address_client)
        if commands[0] == "put":
            #manage parallel access to the following piece of code
            mutex.acquire()
            self.handle_put(commands, new_socket, address_client)

        #release mutual exclusion
        if mutex.locked():
            mutex.release()

    #method that sends the list of files present on the server 
    #to the requesting client
    def handle_list(self, new_socket, address_client):
        new_socket.sendto(str(os.listdir()).encode(), address_client)
        self.write_state_on_file("Correct, list arrived")

    #method that deals with sending a file requested by a client
    #and present on the server
    def handle_get(self, commands, new_socket, address_client):
        new_socket.sendto("ok".encode(), address_client)
        try:
            #the file is split into smaller packets to send
            with open(commands[1], "r") as f:
                data_read = f.read(BUFFER_SIZE)
                new_socket.sendto(data_read.encode(), address_client)
                while True:
                    if not data_read:
                        break
                    data_read = f.read(BUFFER_SIZE)
                    new_socket.sendto(data_read.encode(), address_client)
            self.write_state("Correct, file send")
        except:
            self.close_connection_with_clients(new_socket)
            self.write_state_on_file("Error, to elaborate the file" + commands[1])

    #method that deals with receiving a file sent from a client
    def handle_put(self, commands, new_socket, address_client):
        new_socket.sendto("ok".encode(), address_client)
        try:
            #file is sent in smaller packets until the EOF character is reached
            with open(commands[1], "w") as f:
                data_received, address = new_socket.recvfrom(BUFFER_SIZE)
                f.write(data_received.decode("utf8"))
                while True:
                    #EOF
                    if not data_received:
                        break
                    data_received,address = new_socket.recvfrom(BUFFER_SIZE)
                    f.write(data_received.decode("utf8"))
            self.write_state_on_file("Correct, file received")
        except:
            self.close_connection_with_clients(new_socket)
            self.write_state_on_file("Error, to elaborate the file" + commands[1])

    #close the UDP socket connection
    def close_connection_with_clients(self, new_socket):
        new_socket.close()
