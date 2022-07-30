import os
from sys import version_info
if version_info.major == 2:
    import Tkinter as tk
    from TKinter import messagebox
elif version_info.major == 3:
    import tkinter as tk
    from tkinter import messagebox

STATE_FILE = "temp.txt"

#class that manages the server view
class ViewServer:

    #initialization of the graphic interface
    def __init__(self):
        self.windows_main = tk.Tk()
        self.windows_main.geometry("500x300")
        self.windows_main.title("Server")
        self.windows_main.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.require_server_address()

    #method that deals with loading the page that takes care of acquiring the 
    #ip address and the port number of the server
    def require_server_address(self):
        self.connection_button_state = False
        self.message_frame = tk.Frame(self.windows_main)
        tk.Label(self.message_frame, text = "Insert server address:").pack()        
        tk.Label(self.message_frame, text = "ip address:").pack()
        self.entry_ip = tk.Entry(self.message_frame)
        self.entry_ip.pack()
        tk.Label(self.message_frame, text = "port number:").pack()
        self.entry_port = tk.Entry(self.message_frame)
        self.entry_port.pack()
        self.connection_button = tk.Button(self.message_frame, 
                                           text = "insert",
                                           command=lambda: self.set_connection_button_state(True))
        self.connection_button.pack()
        self.message_frame.pack()

    #method that deals with loading the main graphical interface of the application
    def load_main_page(self):
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
        text = "Server on (ip:" + self.entry_ip.get() + " port:" + self.entry_port.get() + ")"
        self.message_frame.destroy()
        frame_bottom = tk.Frame(self.windows_main)
        tk.Label(frame_bottom, text = text).pack()
        tk.Label(frame_bottom, text = "State of the server").pack()
        self.lbl_state = tk.Label(frame_bottom)
        self.lbl_state.pack(side = tk.TOP)
        frame_bottom.pack(side = tk.TOP)

    #method that reads the information of a file, containing the operations performed 
    #by the server, and displays it in the view
    def update_state_file(self):
        try:
            with open(STATE_FILE, "r") as f:
                lines = f.readlines()
                self.lbl_state["text"] = ""
                for line in lines:
                    self.lbl_state["text"] += line
        except:
            self.lbl_state["text"] = "Wait"

    #method that sets the connection button
    def set_connection_button_state(self, state):
        self.connection_button_state = state
    
    #method that checks if the connect button has been clicked
    def is_connection_button_selected(self):
        if self.connection_button_state:
            self.connection_button_state = False
            return True
        return False

    #method that returns the ip address and port number entered by the user
    def get_address_server(self):
        try:
            return (self.entry_ip.get(), int(self.entry_port.get()))
        except:
            self.show_message("No values")
            return ("00", 0)
    
    #method that shows a message in the view
    def show_message(self, message):
        messagebox.showinfo("Alert", message)

    #method that updates the client view status
    def update(self):
        self.windows_main.update()

    #method that establishes the operations to be performed 
    #when the client is closed
    def on_closing(self):
        self.windows_main.destroy()
        os._exit(-1)
 