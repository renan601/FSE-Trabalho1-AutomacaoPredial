import time
import threading
import signal
import json

from comunication import stablish_communication, receive_data_from_client
from trigger_alarm import trigger_fire_alarm, trigger_system_alarm, trigger_lights
from building_control import building_control
from room_control import room_control, control_menu
from utils import correct_input

class Central:
    def __init__(self):
        self.people_in_room = []
        self.people_in_building = 0
        
        self.client_data = []
        self.outputs = []
        self.inputs = []
        self.temperature_sensor = []
        self.client_rooms = {}

        self.alarm_system = False
        self.fire_alarm = False

        self.prepare_to_connect()
        
        for item in self.client_data:
            item[1].sendall((bytes("Sucesso", encoding='utf-8')))
            thread_listen = threading.Thread(target=self.listen_to_client, args=(item[1], ))
            thread_listen.start()

        self.main_menu()
    
    def prepare_to_connect(self):
        dist_count = int(input('Quantos servidores distribuidos serão conectados? \n'))
        self.connect_to_clients(dist_count)
        
    def connect_to_clients(self, dist_count):
        f = open('ConfigurationFiles/conf.json')
        raspberrys = json.load(f)
        f.close()
        
        for i in range(dist_count):
            print()
            print("Qual placa será conectada ?")
            for key_count, key in enumerate(raspberrys.keys()):
                print(f"{key_count} -- {key}")
            
            choosen_raspberry = correct_input(0, 3)
            
            print("Em qual porta?")
            port = correct_input(1000, 64000)
            print()
            
            com_socket, client_addr, client_room, outputs, inputs, temp_sensor = stablish_communication(list(raspberrys.values())[choosen_raspberry], port)
            self.client_data.append((client_room, com_socket, client_addr))
            self.client_rooms[client_room] = len(self.client_data) - 1
            
            self.outputs.append(outputs)
            self.inputs.append(inputs)
            self.temperature_sensor.append(temp_sensor)
            self.people_in_room.append(0)

            print(f"Conectado ao servidor correspondente a {client_room} \n")
    
    
    def listen_to_client(self, com_socket):
        possible_types = {
            "Lâmpada 01": 0,
            "Lâmpada 02": 1,
            "Projetor Multimidia": 2,
            "Ar-Condicionado (1º Andar)": 3,
            "Sirene do Alarme": 4,
            
            "Sensor de Presença": 10,
            "Sensor de Fumaça": 11,
            "Sensor de Janela": 12,
            "Sensor de Porta": 13,
            "Sensor de Contagem de Pessoas Entrada": 14,
            "Sensor de Contagem de Pessoas Saída": 15,

            "Sensor de Temperatura e Umidade": 20,
        }

        while True:
            data = receive_data_from_client(com_socket)
            room_name = data['room_name']
            room_position_on_list = self.client_rooms.get(room_name)

            if data.get('status', False) == True:
                print(f"Ação em {data['tag']} da sala {data['room_name']} realizada com sucesso")
            
            for key, value in possible_types.items():
                if data['tag'] == key:
                    if value < 10:
                        self.outputs[room_position_on_list][value]['value'] = data['value']
                    elif value < 20:
                        self.inputs[room_position_on_list][value-10]['value'] = data['value']
                        self.people_in_room[room_position_on_list] = data.get('people_in_room')
                        self.people_in_building = sum(self.people_in_room)
                        
                        trigger_fire_alarm(data, self.fire_alarm, self.client_rooms, self.client_data, self.outputs)
                        trigger_system_alarm(data, self.alarm_system, self.client_rooms, self.client_data, self.outputs)
                        trigger_lights(data, self.alarm_system, room_position_on_list, self.client_data, self.outputs)

                    elif value < 30:
                        self.temperature_sensor[room_position_on_list][value-20]['temp'] = data['temp']
                        self.temperature_sensor[room_position_on_list][value-20]['humidity'] = data['humidity']

    
    def main_menu(self):
        menu = {}
        
        for j, item_output in enumerate(self.outputs[0]):
            if item_output['type'] != 'alarme':
                menu[j] = (f"Ligar/Desligar {item_output['tag']}")
        
        while True:
            print("1 - Visualizar estado do sistema.")
            print("2 - Acionar/Desligar dispositivos em uma sala.")
            print("3 - Acionar/Desligar dispositivos no prédio.")
            print("4 - Interromper o programa.")
            action = int(input("Escolha uma das opções acima. \n"))
            
            if action == 1:
                try:
                    self.display()
                except:
                    print("\n")
                    continue
            elif action == 2:
                room = room_control(self)
                control_menu(self, room, menu)
                print("\n")
            elif action == 3:
                building_control(self)
            else:
                exit()

    def display(self):
        def handler_signal(signum, frame):
            raise Exception

        signal.signal(signal.SIGINT, handler_signal)

        old_inputs = list(range(0, len(self.client_data)))
        old_outputs = list(range(0, len(self.client_data)))

        while True:
            for i in range(len(self.client_data)):
                if old_outputs[i] != str(self.outputs[i]) or old_inputs[i] != str(self.inputs[i]):
                    print(f"Sistema {self.client_data[i][0]}")

                    for item_output in self.outputs[i]:
                        print(f"Valor {item_output['tag']}: {item_output.get('value', 'False')}")
                    
                    for item_input in self.inputs[i]:
                        if item_input['type'] != 'contagem':
                            print(f"Valor {item_input['tag']}: {item_input.get('value', 'Não Identificado')} ")
                    
                    print(f"People in room: {self.people_in_room[i]}")
                    
                    for temp_sensor in self.temperature_sensor[i]:
                        print(f"Temperatura: {temp_sensor.get('temp', 'Não Identificado')}")
                        print(f"Umidade: {temp_sensor.get('humidity', 'Não Identificado')}")

                    print(f"People in the building: {self.people_in_building}")
                    print()
                    print("Aperte Ctlr C para voltar ao menu principal")
                    print()

                    old_outputs[i] = str(self.outputs[i])
                    old_inputs[i] = str(self.inputs[i])

            time.sleep(1)


if __name__=='__main__':
    Central()