from ViewServer import ViewServer
from ModelServer import ModelServer
from threading import Thread

#class representing the application server
class Server:
    def run():
        #instantiate the graphics and logic of the server
        view = ViewServer()
        model = ModelServer()

        #acquisition of the address of the server
        while True:
            if view.is_connection_button_selected():
                address, port = view.get_address_server()
                #check if the server address can be accepted
                if not model.set_server_address(address, port):
                    view.show_message("Ip address or port number are wrong")
                else:
                    view.load_main_page()
                    break
            view.update()
        
        model.set_server_address(address, port)
        
        #the management of client requests are handled in a thread
        handle_thread = Thread(target = model.handle, args=(view,))
        
        #thread stops when main thread dies
        handle_thread.daemon = True
        handle_thread.start()
        
        #show in the view the operations performed by the server
        while True:
            view.update_state_file()
            view.update()
        
    run()