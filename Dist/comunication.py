import socket
import json
import time

def stablish_communication(room_name, conf_file):
    HOST = conf_file['ip_servidor_distribuido']
    PORT = conf_file['porta_servidor_distribuido']

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    com_socket, addr = s.accept()
    
    com_socket.sendall(bytes(room_name, encoding='utf-8'))
    resp = com_socket.recv(1024)
    com_socket.sendall(bytes(json.dumps(conf_file['outputs']), encoding='utf-8'))
    resp = com_socket.recv(1024)
    com_socket.sendall(bytes(json.dumps(conf_file['inputs']), encoding='utf-8'))
    resp = com_socket.recv(1024)
    com_socket.sendall(bytes(json.dumps(conf_file['sensor_temperatura']), encoding='utf-8'))
    resp = com_socket.recv(1024)
    
    print(f"Waiting connection from other distributed servers")
    resp = com_socket.recv(1024)
    
    print(f"Connected by {addr} \n\n")
    return com_socket

def send_data_to_central(com_socket, data):
    com_socket.sendall(bytes(json.dumps(data), encoding='utf-8'))

def receive_data_from_central(com_socket):
    data = com_socket.recv(1024)
    return json.loads(data)