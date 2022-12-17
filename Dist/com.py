import socket
import json

def stablish_communication(room_name):
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    com_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    com_socket.connect((HOST, PORT))
    com_socket.sendall(bytes(room_name, encoding='utf-8'))
    return com_socket

def send_data_to_central(com_socket, data):
    com_socket.sendall(bytes(json.dumps(data)), encoding='utf-8')
    print(f"Send {data!r}")

def receive_data_from_central(com_socket):
    data = com_socket.recv(1024)
    return data