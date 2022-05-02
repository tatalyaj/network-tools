#   Template - client side
#   Author: Talya Shaltiel, 2020
#   IN ORDER to gets client- server first activate server then client

import socket
import protocol


IP = "127.0.0.1"
# The path + filename where the copy of the screenshot at the client should be saved
#                   *****   PATHS! *****
SAVED_PHOTO_LOCATION = r"C:\Users\tatal\OneDrive\Documents\College\client_screen_shots\photo.jpg"
#                       ENDPATHS


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    cmd_line = cmd.split(" ")
    command = cmd_line[0]
    valid_srv_response, server_response = protocol.get_msg(my_socket)
    if valid_srv_response:
        if command == 'SEND_PHOTO':
            image_file = open(SAVED_PHOTO_LOCATION, 'wb')
            # Here server_response is the size of the binary file
            data = my_socket.recv(int(server_response))  # will read the size of the bin file
            if not data:
                image_file.close()
            image_file.write(data)
            image_file.close()
            print("The Image has been send successfully")
        # all other responses except SEND_PHOTO
        elif command == "EXIT":
            print("The server's response is: " + server_response)
        else:
            print("The server's response is: " + server_response)

    else:
        print("Response not valid\n")


def main():
    # opens socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, protocol.PORT))
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet)
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    print("Closing\n")
    my_socket.close()


if __name__ == '__main__':
    main()
