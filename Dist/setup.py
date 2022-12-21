from utils import correct_input
import json
import socket
import time

def setup():
    hostname = socket.gethostname()

    print(f"Voce está se conectando a placa {hostname} \n")

    if hostname == "rasp47" or hostname == "rasp46":
        f = open('ConfigurationFiles/conf_sala_1.json')
        print(f"O arquivo de configuração conf_sala_1.json será utilizado.")
        print(f"Certifique-se de que o IP do servidor e a porta estão corretamente preenchidos.")
    else:
        f = open('ConfigurationFiles/conf_sala_2.json')
        print(f"O arquivo de configuração conf_sala_2.json será utilizado.")
        print(f"Certifique-se de que o IP do servidor e a porta estão corretamente preenchidos.")

    print("O nome da sala deve ser único para cada servidor distribuído.")
    time.sleep(2)
    data = json.load(f)
    f.close()

    return data