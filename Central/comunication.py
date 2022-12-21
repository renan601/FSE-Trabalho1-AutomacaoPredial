import socket
import json

def stablish_communication(raspberry, port):
    HOST = raspberry
    PORT = port
    
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"Tentativa de conexão no IP {raspberry} e porta {port}")
    conn.connect((HOST, PORT))
    
    room_name = conn.recv(1024)
    conn.sendall((bytes("Sucesso", encoding='utf-8')))
    
    outputs = conn.recv(1024)
    conn.sendall((bytes("Sucesso", encoding='utf-8')))

    inputs = conn.recv(1024)
    conn.sendall((bytes("Sucesso", encoding='utf-8')))
    
    temp_sensor = conn.recv(1024)
    conn.sendall((bytes("Sucesso", encoding='utf-8')))
    
    return conn, "", str(room_name, encoding='utf-8'), json.loads(outputs), json.loads(inputs), json.loads(temp_sensor)

def send_data_to_client(data, conn, addr):
    sensor_status = (bytes(json.dumps(data), encoding='utf-8'))
    conn.sendall(sensor_status)

def receive_data_from_client(conn):
    data = conn.recv(1024)
    return json.loads(data)