#   Template - protocol
#   Author: Talya Shaltiel, 2020

LENGTH_FIELD_SIZE = 4
PORT = 8820
COMMAND_LIST = ["SEND_PHOTO", "TAKE_SCREENSHOT", "EXIT", "DIR", "DELETE", "EXECUTE", "COPY"]


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    # arg_list[0]
    arg_list = data.split(" ")

    # Has 0 Parameters :Send_photo, Take_Screenshot, EXIT
    if len(arg_list) == 1:
        if arg_list[0] == COMMAND_LIST[0]:  # "SEND_PHOTO"
            return True
        elif arg_list[0] == COMMAND_LIST[1]:  # "TAKE_SCREENSHOT"
            return True
        elif arg_list[0] == COMMAND_LIST[2]:  # "EXIT
            return True
    # Has one Parameter: Delete, Dir, Execute
    elif len(arg_list) == 2:
        if arg_list[0] == COMMAND_LIST[3]:  # "DIR"
            return True
        elif arg_list[0] == COMMAND_LIST[4]:  # "DELETE"
            return True
        elif arg_list[0] == COMMAND_LIST[5]:  # "EXECUTE"
            return True
    elif len(arg_list) == 3 and arg_list[0] == COMMAND_LIST[6]:  # "COPY"
        # Has 2 Parameters: Copy
        return True
    else:
        return False


def create_msg(data):
    """
    Create a valid protocol message, with length field, ex: returns "0002OK".encode()
    """
    if isinstance(data, int):  # In case the command is SEND_PHOTO, all the data is an int number
        # ex: data = len of photo, ex: 2000000
        photo_size_length = len(str(data))  # The length of the  photo size, ex: 7
        zfill_photo_size_length = str(photo_size_length).zfill(LENGTH_FIELD_SIZE)
        #  The length of the  photo size with zeros :- length field, ex: 0007
        data = zfill_photo_size_length + str(data)  # length field + photo size, ex: 00072000000
    else:  # Any other case
        length = str(len(data))
        zfill_length = length.zfill(LENGTH_FIELD_SIZE)
        data = zfill_length + data
    return data.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field(return "OK")
    If length field does not include a number, returns False, "Error"
    """
    length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    message = my_socket.recv(int(length)).decode()
    if length.isdigit:
        return True, message
    else:
        return False, "Error"



