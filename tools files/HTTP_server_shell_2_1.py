# HTTP Server Shell
# Author: Talya Shaltiel
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# It demonstrates a part in the way HTTP works.
# There's examples for various status codes such as : 200 0k(loaded successfully), 500(Internal Server Error) etc'...


import socket
import codecs
import os
#              *****   PATHS! *****
DEFAULT_URL = r"C:\Networks\work\webroot\index.html"
CHANGED_INITIAL_DICTIONARY = r"C:\Networks\work\webroot\folder\index.html"
INITIAL_DICTIONARY = r"/page1.html"
REDIRECTION_DICTIONARY = {
   r"C:\Networks\work\webroot\index.html": "/Networks/work/webroot/index.html",
   r"C:\Networks\work\webroot\folder\index.html": "/Networks/work/webroot/index.html"
                        }
FORBIDDEN_FILE = r"/forbidden_file.txt"
FORBIDDEN_FILE_ORIGIN_LOCATION = r"\\forbidden_file.txt"
#                   ENDPATHS

PORT = 80
# PORT = 5000
IP = "0.0.0.0"
SOCKET_TIMEOUT = 5
CR_LF = '\r\n'
ERROR_MESSAGE = "ERROR"
HTTP_VERSION = "HTTP/1.1"
HTTP_METHOD = "GET"
HEADER_LIST = ["Content-Type: ", "Content-Length: ", "Location: "]
STATUS_CODE_LIST = [200, 302, 403, 500, 404]
PHRASE_LIST = ["OK", "Found", "Forbidden", "Internal Server Error", "Not Found"]


#  ~ The following 5 functions generate the proper status line, which will be called when needed ~

def ok_status_line():
    # status line:VERSION 200 OK\r\n
    http_status_line = HTTP_VERSION + " " + str(STATUS_CODE_LIST[0]) + " "
    # VERSION 200
    http_status_line = http_status_line + PHRASE_LIST[0] + CR_LF
    #  OK\r\n
    return http_status_line


def moved_status_line():
    # status line:VERSION  302  Found\r\n
    http_status_line = HTTP_VERSION + " " + str(STATUS_CODE_LIST[1]) + " "
    # VERSION Status Code: 302
    http_status_line = http_status_line + PHRASE_LIST[1] + CR_LF
    #  Moved Temporarily\r\n
    return http_status_line


def forbidden_status_line():
    # status line:VERSION  403  Forbidden\r\n
    http_status_line = HTTP_VERSION + " " + str(STATUS_CODE_LIST[2]) + " "
    # VERSION 403
    http_status_line = http_status_line + PHRASE_LIST[2] + CR_LF
    #  Forbidden\r\n
    return http_status_line


def not_found_status_line():
    # status line:VERSION 404  Not Found\r\n
    http_status_line = HTTP_VERSION + " " + str(STATUS_CODE_LIST[4]) + " "
    # VERSION 404
    http_status_line = http_status_line + PHRASE_LIST[4] + CR_LF
    #  Not Found\r\n
    return http_status_line


def server_error_status_line():
    # status line:VERSION 500  Interval Server Error\r\n
    http_status_line = HTTP_VERSION + " " + str(STATUS_CODE_LIST[3]) + " "
    # VERSION 500
    http_status_line = http_status_line + PHRASE_LIST[3] + CR_LF
    #  Interval Server Error\r\n
    return http_status_line


# This func reads and gets the data from the resource
def get_file_data(filename):
    """ Get data from file """
    file_origin_location = filename.replace("/", "\\")  # replacing / (internet form) into \\ (windows form)

    # file_origin_location - is the windows form, the location of the file itself
    if file_origin_location.endswith(".jpg") or file_origin_location.endswith(".ico"):  # image, ico
        input_file = open(file_origin_location, "rb")
        data = input_file.read()
    elif file_origin_location.endswith(".html") or file_origin_location.endswith(".css"):  # html, css
        input_file = codecs.open(file_origin_location, "r", "utf-8")
        # input_file = codecs.open(file_origin_location, "r")
        data = input_file.read()
    elif file_origin_location.endswith(".txt") or file_origin_location.endswith(".js"):  # txt, js
        input_file = open(file_origin_location, "r")
        data = input_file.read()
    return data


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    file_exist = os.path.exists(resource)
    if file_exist:
        # An example of redirected URL
        if resource == '/':
            url = DEFAULT_URL

        # Another example for redirected URL
        elif resource == INITIAL_DICTIONARY:
            url = CHANGED_INITIAL_DICTIONARY
        else:
            url = resource
            # (Here there is the internet form - the name of the file)

        # Concerning the Redirected URL -  checks and sends proper response
        if url in REDIRECTION_DICTIONARY:
            http_status_line = moved_status_line()
            http_location_header = HEADER_LIST[2] + REDIRECTION_DICTIONARY[url] + CR_LF
            http_response = http_status_line + http_location_header + CR_LF
            client_socket.send(http_response.encode())
            return
        # Concerning the forbidden file URL - checks and sends proper response
        elif url == FORBIDDEN_FILE:
            try:
                open(FORBIDDEN_FILE)
            except PermissionError:
                http_status_line = forbidden_status_line()
                http_response = http_status_line + CR_LF
                client_socket.send(http_response.encode())
                return
        else:
            http_status_line = ok_status_line()

            # Extracting requested file type from URL -> Content-Type: x\r\n
        if url.endswith(".html") or url.endswith(".txt"):
            http_content_header = HEADER_LIST[0] + "text/html; charset=utf-8" + CR_LF
            # Content-Type: text/html; charset=utf-8"
        elif url.endswith(".js"):
            # Generating proper HTTP header
            http_content_header = HEADER_LIST[0] + "text/javascript; charset=UTF-8" + CR_LF
            # Content-Type: text/javascript; charset=UTF-8
        elif url.endswith(".css"):
            # Generating proper HTTP header
            http_content_header = HEADER_LIST[0] + "text/css" + CR_LF
            # Content-Type: text/css
        elif url.endswith(".jpg") or url.endswith(".ico"):
            # Generating proper HTTP header
            http_content_header = HEADER_LIST[0] + "image/jpeg" + CR_LF
            # Content-Type: image/jpeg

        # Getting the data itself - and puts it inside of data variable
        filename = url
        data = get_file_data(filename)
        # Getting the content's Length - > Content-Length: x\r\n
        data_length = len(data)
        http_content_length_header = HEADER_LIST[1] + str(data_length) + CR_LF
        # Sending the data
        # Separating it into 2 cases, 1: if the data is an image type 2: the rest types of data
        if url.endswith(".jpg") or url.endswith(".ico"):
            http_response = http_status_line + http_content_header + http_content_length_header + CR_LF
            # Transforming response without data to binary so we could add them
            http_response = http_response.encode()
            http_response = http_response + data
            # Sending to the Socket without encoding cause its already in a binary format
            client_socket.send(http_response)
        else:
            http_response = http_status_line + http_content_header + http_content_length_header + CR_LF + data
            client_socket.send(http_response.encode())
    else:
        # If the file doesn't exist the answer is : 404 Not Found
        http_status_line = not_found_status_line()
        http_response = http_status_line + CR_LF
        client_socket.send(http_response.encode())


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """

    if request.count(CR_LF) >= 2:
        combined_line_list = request.splitlines()  # Separates with spaces
        separate_str_list = combined_line_list[0].split(" ")
        if len(separate_str_list) == 3:
            for i in range(len(separate_str_list)):
                if separate_str_list[0] == HTTP_METHOD:
                    if separate_str_list[2] == HTTP_VERSION:
                        requested_url = separate_str_list[1]  # in Requested_url : separate_str_list[1] which is the URL
                        return True, requested_url  # Name of URL, (internet form)
    return False, ERROR_MESSAGE


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    while True:
        # In case the timeout of the socket is expired, there's an except that acts accordingly
        try:
            client_request = client_socket.recv(1024).decode()
            valid_http, resource = validate_http_request(client_request)
            if valid_http:
                print('Got a valid HTTP request')
                handle_client_request(resource, client_socket)
                break
            else:
                print('Error: Not a valid HTTP request')
                # when request isn't valid: 500 Interval Server Error
                http_status_line = server_error_status_line()
                http_response = http_status_line + CR_LF
                client_socket.send(http_response.encode())
                break
        except socket.timeout:
            print("Socket timeout")
    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)

        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
