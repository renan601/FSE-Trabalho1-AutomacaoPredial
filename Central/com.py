import socket
import json

def stablish_communication():
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 10062  # Port to listen on (non-privileged ports are > 1023)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    room_name = conn.recv(1024)
    print(f"Connected by {addr}, room name {str(room_name, encoding='utf-8')}")
    return conn, addr, str(room_name, encoding='utf-8')

def send_data_to_client(data, conn, addr):
    print(f"Send data to client {addr}")
    sensor_status = (bytes(json.dumps(data), encoding='utf-8'))
    conn.sendall(sensor_status)

def receive_data_from_client(conn):
    print(f"Receive data from client")
    data = conn.recv(1024)
    return json.loads(data)