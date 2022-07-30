from ViewClient import ViewClient
from ModelClient import ModelClient
from pathlib import Path

#class representing the application client
class Client:
    def run():
        #instantiate the graphics and logic of the client
        view = ViewClient()
        model = ModelClient()
        
        #acquisition of the address of the server to which the client will have to connect
        while True:
            #by clicking on the appropriate button an attempt is made to 
            #establish a connection with the server to check if its address is correct
            if view.is_connection_button_selected():
                if not model.connection_with_server(view.get_address_server()):
                    view.show_message("Connection with server failed")
                else:
                    #if the server exists, the main page is loaded
                    view.load_main_page()
                    break
            #refresh of the view
            view.update()

        while True:
            #sending the request for the list of files on the server and 
            #receiving it by showing it in the view
            if view.is_list_button_selected():
                view.set_server_files(model.list_server_files())
            
            #by clicking on the relative button the download of the file 
            #selected from the view and present on the server is managed
            if view.is_download_button_selected():
                #check if the file list contains any elements
                if view.get_selected_file() == "":
                    view.show_message("There isn't a selected file")
                    continue
                #request the location to store the downloaded file
                try:
                    path_file = view.get_path_dialog_file()
                except:
                    view.show_message("Error in the download of the file")
                    continue
                
                #proceed with the download of the file
                message = model.download_selected_file(view.get_selected_file(),
                                                       path_file)
                view.show_message(message)

            #by clicking on the relative button the upload of a file from the 
            #client to the server is managed
            if view.is_upload_button_selected():
                #acquisition of the file to be sent to the server
                try:
                    path_file = view.get_path_file()
                except:
                    view.show_message("Error in the upload of the file")
                    continue
                #proceed with the upload of the file
                message = model.upload_file(path_file, 
                                            Path(path_file).name)
                view.show_message(message)
            #refresh of the view
            view.update()
            

    run()