#   Template - server side
#   Author:Talya Shaltiel, 2020
#   IN ORDER to gets client- server first activate server then client


import socket
import protocol
import os
import glob
import shutil
import subprocess
import pyautogui

IP = "0.0.0.0"
# The path + filename where the screenshot at the server should be saved
#                       *****   PATHS! *****
PHOTO_PATH = r"C:\Users\tatal\OneDrive\Documents\College\server_screen_shots\photo.jpg"
#                           ENDPATHS
ERROR_MESSAGE = "ERROR"


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """

    # Use protocol.check_cmd first
    valid_cmd = protocol.check_cmd(cmd)
    if valid_cmd:  # command and num of params correct
        # Then make sure the params are valid
        cmd_line = cmd.split(" ")
        command = cmd_line[0]
        params = []
        if command == "COPY" or command == "DELETE" or command == "EXECUTE" or command == "DIR":
            params = cmd_line[1:]
            check_params = os.path.exists(params[0])  # Checks that the files/ directory exist
            if check_params:  # If they exist
                return True, command, params
            else:
                return False, ERROR_MESSAGE, params
        else:
            return True, command, params  # for EXIT TAKESCREENSHOT, SENDPHOTO, EXIT  params=[]
    else:
        return False, ERROR_MESSAGE, ERROR_MESSAGE


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """

    if command == "DIR":
        files_list = glob.glob(params[0] + "\\*.*")  # Getting the files list from a given directory
        files_list_into_str = ' '.join([str(item) for item in files_list])  # turning files list into str
        response = files_list_into_str.replace(params[0] + "\\", '')  # removing the path from the files
    elif command == "COPY":
        shutil.copy(params[0], params[1])  # Copying first file  into second file
        response = "The File has been copied"
    elif command == "DELETE":
        os.remove(params[0])  # Deleting given file
        response = "The File has been deleted"
    elif command == "EXECUTE":
        subprocess.call(params[0])  # Executing a given path of executable file
        response = "The program has been executed"
    elif command == "TAKE_SCREENSHOT":
        image = pyautogui.screenshot()  # Taking a screen shot
        image.save(PHOTO_PATH)
        response = "The image has been taken"
    elif command == "SEND_PHOTO":
        my_file = open(PHOTO_PATH, "rb")  # reading data from the photo that was taken
        file_bytes = my_file.read()
        photo_size = len(file_bytes)
        response = photo_size  # eventually sending photo size

    return response


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")
    # handles requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                if command == 'EXIT':
                    break
                # prepare a response using "handle_client_request"
                response = handle_client_request(command, params)
                # add length field using "create_msg"
                response = protocol.create_msg(response)
                # send to client
                client_socket.send(response)
                if command == 'SEND_PHOTO':
                    # After the photo size has been sent from handle_client_request func,
                    # The photo/data itself  will be Sent to the client
                    photo_file = open(PHOTO_PATH, "rb")
                    photo_bytes = photo_file.read()
                    client_socket.send(photo_bytes)

            else:
                # prepare proper error to client
                response = "Bad command or parameters"
                response = protocol.create_msg(response)
                # send to client
                client_socket.send(response)

        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            # send to client
            response = protocol.create_msg(response)
            # send to client
            client_socket.send(response)
            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    response = "Closing connection"
    response = protocol.create_msg(response)
    # send to client
    client_socket.send(response)
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
