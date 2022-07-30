import socket as sk

BUFFER_SIZE = 4096

#class that manages the client logic
class ModelClient:
    
    def __init__(self):
        #create the UDP socket
        self.sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    
    #method where it is checked that the server's ip address 
    #and port number are correct
    def connection_with_server(self, address):
        try:
            #send the check command to the server and put the client 
            #waiting for a response
            self.address = address
            self.send_message("check")
            self.sock.settimeout(2.0)
            message, addr = self.sock.recvfrom(BUFFER_SIZE)
            #if the client receives a correct answer, it returns true
            if(message.decode("utf8") != "ok"):
               return False
        except sk.timeout:
            #if the client does not receive a response within the expected 
            #time period, it is returned false
            self.sock.settimeout(None)
            return False
        except:
            return False
        return True
    
    #method that request to the server for a list of its files
    def list_server_files(self):
        print("send command list")
        #send the command list
        self.send_message("list")
        # the client waits for a response from the server, containing the 
        # list of files
        data, address = self.sock.recvfrom(BUFFER_SIZE)
        print("receive list of files from the server")
        list_of_files = data.decode()
        list_of_files = list_of_files[1:len(list_of_files) - 1]
        list_of_files = list_of_files.replace("'", "")
        return list_of_files.split(", ")
    
    #method that deals with the download of a specified file, present on the server, 
    #in the folder specified by the user
    def download_selected_file(self, file_name, destination_path):
        #send the get command to the server followed by the name of the file 
        #that the client wants to receive from the server
        print("send command get")
        command = "get " + file_name + " "
        self.send_message(command)
        print("receive ok command")
        
        #the client receives the response from the server
        command, address = self.sock.recvfrom(BUFFER_SIZE)
        if command.decode("utf8") != "ok":
            return "Error, command different from ok"

        try:
            with open(destination_path, "w") as f:
                # the client receives the file split into packets 
                #until EOF is reached
                data_read, address = self.sock.recvfrom(BUFFER_SIZE)
                f.write(data_read.decode("utf8"))
                while True:
                    #received EOF
                    if not data_read:
                        break
                    data_read, address = self.sock.recvfrom(BUFFER_SIZE)
                    f.write(data_read.decode("utf8"))
            message = "File received successfully"
        except:
            message = "File download error"
        return message
    
    #method that deals with uploading a file from client to server
    def upload_file(self, source_file, file_name):
        #sending the put command followed by the name of the file that the 
        #client wants to send to the server
        command = "put " + file_name + " "
        self.send_message(command)
        
        #the client receives the response from the server
        print("receive ok command")
        command, address = self.sock.recvfrom(BUFFER_SIZE)
        if command.decode("utf8") != "ok":
            return "Error, command different from ok"

        try:
            with open(source_file, "r") as f:
                # the client receives the file split into packets 
                #until EOF is reached
                data_read = f.read(BUFFER_SIZE)
                self.sock.sendto(data_read.encode(), address)
                while True:
                    #received EOF
                    if not data_read:   
                        self.sock.sendto(data_read.encode(), address)
                        break
                    data_read = f.read(BUFFER_SIZE)
                    self.sock.sendto(data_read.encode(), address)
                message = "File sent successfully"
        except:
            message = "File upload error"
        return message

    #method that deals with sending a command from the client to the server
    def send_message(self, message):
        self.sock.sendto(str(message).encode("utf8"), self.address)
    
    #closing the socket used to send data to the server
    def close_connection_with_server(self):
        self.sock.close()
