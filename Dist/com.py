import socket
import json

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

json_ex = {
    "outputs": [
        {
            "type": "lampada",
            "tag": "Lâmpada 01",
            "gpio": 18,
            "value": 1
        },
        {
            "type": "lampada",
            "tag": "Lâmpada 02",
            "gpio": 23,
        },
        {
            "type": "projetor",
            "tag": "Projetor Multimidia",
            "gpio": 25,
        },
        {
            "type": "ar-condicionado",
            "tag": "Ar-Condicionado (1º Andar)",
            "gpio": 24,
        },
        {
            "type": "alarme",
            "tag": "Sirene do Alarme",
            "gpio": 8,
        }
    ],
    "inputs": [
        {
            "type": "presenca",
            "tag": "Sensor de Presença",
            "gpio": 7,
        },
        {
            "type": "fumaca",
            "tag": "Sensor de Fumaça",
            "gpio": 1,
        },
        {
            "type": "janela",
            "tag": "Sensor de Janela",
            "gpio": 12,
        },
        {
            "type": "porta",
            "tag": "Sensor de Porta",
            "gpio": 16,
        },
        {
            "type": "contagem",
            "tag": "Sensor de Contagem de Pessoas Entrada",
            "gpio": 20,
            "value": 1
        },
        {
            "type": "contagem",
            "tag": "Sensor de Contagem de Pessoas Saída",
            "gpio": 21,
            "value": 1
        }
    ],
    "sensor_temperatura":[
        {
        "type": "dth22",
        "tag": "Sensor de Temperatura e Umidade",
        "gpio": 4,
        "value": 1
        }
    ]
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #for _ in range(3):
    s.sendall(bytes(json.dumps(json_ex), 'utf-8'))
    data = s.recv(1024)

print(f"Received {data!r}")