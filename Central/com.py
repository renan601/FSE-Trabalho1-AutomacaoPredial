import socket
import json

def stablish_communication():
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    room_name = conn.recv(1024)
    return conn, addr, room_name

def send_data_to_client(data, conn, addr):
    import ipdb; ipdb.set_trace()
    print(f"Connected by {addr}")
    sensor_status = (bytes(json.dumps(data), encoding='utf-8'))
    conn.sendall(sensor_status)
    #client_data = conn.recv(1024)

def receive_data_from_client():
    pass
