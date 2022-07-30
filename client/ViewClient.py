import os
from sys import version_info
if version_info.major == 2:
    import Tkinter as tk
    import Tkinter.ttk as ttk
    import TKinter.filedialog as filedialog
elif version_info.major == 3:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.filedialog as filedialog

#class that manages the client view
class ViewClient:
    
    #initialization of the graphic interface
    def __init__(self):
        self.list_button_state = False
        self.download_button_state = False
        self.upload_button_state = False
        self.windows_main = tk.Tk()
        self.windows_main.geometry("500x300")
        self.windows_main.title("Client")
        self.windows_main.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.require_server_address()

    #method that deals with loading the page that takes care of acquiring the 
    #ip address and the port number of the server to which the client intends to connect
    def require_server_address(self):
        self.connection_button_state = False
        self.message_frame = tk.Frame(self.windows_main)
        tk.Label(self.message_frame, text = "Insert client address:").pack()
        tk.Label(self.message_frame, text = "ip address:").pack()
        self.entry_ip = tk.Entry(self.message_frame)
        self.entry_ip.pack()
        tk.Label(self.message_frame, text = "port number:").pack()
        self.entry_port = tk.Entry(self.message_frame)
        self.entry_port.pack()
        self.connection_button = tk.Button(self.message_frame, 
                                           text = "insert", 
                                           command=lambda: self.set_button_state("connection", True))
        self.connection_button.pack()
        self.message_frame.pack()

    #method that deals with loading the main graphical interface of the application
    def load_main_page(self):
        self.message_frame.destroy()
        top_frame = tk.Frame(self.windows_main)
        lbl_name = tk.Label(top_frame, text = "Client:")
        lbl_name.pack(side = tk.TOP)
        top_frame.pack(side= tk.TOP)
        
        left_frame = tk.Frame(self.windows_main)
        lbl_files = tk.Label(left_frame, text = "Server files:")
        lbl_files.pack(side = tk.TOP)
        self.combo_box = ttk.Combobox(left_frame)
        self.combo_box.pack(side = tk.BOTTOM)
        left_frame.pack(side = tk.LEFT)
        
        right_frame = tk.Frame(self.windows_main)
        list_button = tk.Button(right_frame, text = "List of server files", command=lambda: self.set_button_state("list", True))
        list_button.pack(side = tk.TOP)
        download_button = tk.Button(right_frame, text = "Download Selected File", command=lambda: self.set_button_state("download", True))
        download_button.pack(side = tk.TOP)
        upload_button = tk.Button(right_frame, text = "Upload a file" , command=lambda: self.set_button_state("upload", True))
        upload_button.pack(side = tk.TOP)
        right_frame.pack(side = tk.RIGHT)

    #method that returns the ip address and port number entered by the user
    def get_address_server(self):
        try:
            return (self.entry_ip.get(), int(self.entry_port.get()))
        except:
            self.show_message("No values")

    #method used to notify when a button is clicked
    def set_button_state(self, index_state, state):
        if index_state == "connection":
            self.connection_button_state = state
        if index_state == "list":
            self.list_button_state = state
        if index_state == "download":
           self.download_button_state = state
        if index_state == "upload":
           self.upload_button_state = state
    
    #method used to check if a button was clicked
    def is_button_selected(self, index_state):
        if index_state == "connection" and self.connection_button_state:
            self.connection_button_state = False
            return True
        if index_state == "list" and self.list_button_state:
            self.list_button_state = False
            return True
        if index_state == "download" and self.download_button_state:
            self.download_button_state = False
            return True
        if index_state == "upload" and self.upload_button_state:
            self.upload_button_state = False
            return True
        return False
    
    #method used to show a message to the user
    def show_message(self, message):
        tk.messagebox.showinfo("Alert", message)

    #method that checks if the connect button has been clicked
    def is_connection_button_selected(self):
        return self.is_button_selected("connection")
    
    #method that checks if the list button has been clicked
    def is_list_button_selected(self):
        return self.is_button_selected("list")
    
    #method that checks if the download button has been clicked
    def is_download_button_selected(self):
        return self.is_button_selected("download")
    
    #method that checks if the upload button has been clicked
    def is_upload_button_selected(self):
        return self.is_button_selected("upload")
    
    #method that acquires the path of a file
    def get_path_dialog_file(self):
        return filedialog.asksaveasfile().name

    #method that establishes the path of a new file
    def get_path_file(self):
        return filedialog.askopenfile(filetypes=[("Python","*.py")]).name
    
    #method that shows the list of files present on the server
    def set_server_files(self, files):
        self.combo_box['values'] = files
        if len(files) <= 0:
            self.combo_box["state"] = False
        else:
            self.combo_box["state"] = True
            self.combo_box.set(files[0])

    #method that returns the selected file    
    def get_selected_file(self):
         return self.combo_box.get()

    #method that establishes the operations to be performed 
    #when the client is closed
    def on_closing(self):
        self.windows_main.destroy()
        os._exit(-1)

    #method that updates the client view status
    def update(self):
        self.windows_main.update()