from com import stablish_communication, send_data_to_client, receive_data_from_client
import json
import time
import threading

class Central:
    def __init__(self, conf_file):
        self.outputs = conf_file["outputs"]
        self.inputs = conf_file["inputs"]
        self.temperature_sensor = conf_file["sensor_temperatura"]

        self.client_data = []

        self.connect_to_clients()
        
        for item in self.client_data:
            thread_listen = threading.Thread(target=self.listen_to_client, args=(item[1], ))
            thread_listen.start()

        self.main_menu()
    
    def connect_to_clients(self):
        dist_count = int(input('Quantos servidores distribuidos serão conectados? \n'))

        for i in range(dist_count):
            com_socket, client_addr, client_room = stablish_communication()
            self.client_data.append((client_room, com_socket, client_addr))
    
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
            
            for key, value in possible_types.items():
                if data['tag'] == key:
                    if value < 10:
                        self.outputs[value]['value'] = data['value']
                    elif value < 20:
                        self.inputs[value-10]['value'] = data['value']
                    elif value < 30:
                        self.temperature_sensor[value-20]['value'] = data['value']

    def main_menu(self):
        menu = {}
        
        for j, item_output in enumerate(self.outputs):
            menu[j] = (f"Ligar/Desligar {item_output['tag']}")
        
        while True:
            print("1 - Visualizar estado do sistema.")
            print("2 - Alterar estado do sistema.")
            action = int(input("Escolha uma das opções acima. \n"))
            
            if action == 1:
                self.display()
                print("\n")
            elif action == 2:
                self.control_menu(menu)
                print("\n")
            else:
                exit()


    def display(self):
        for i in range(len(self.client_data)):
            print(self.inputs)
            print(f"Sistema {self.client_data[i][0]}")

            for item_output in self.outputs:
                print(f"Valor {item_output['tag']}: {item_output['value']}")
            
            for item_input in self.inputs:
                print(f"Valor {item_input['tag']}: {item_input.get('value', 'Não Identificado')} ")
            
            #for temp_sensor in self.temperature_sensor:
                #print(f"Valor {temp_sensor['tag']}: {temp_sensor.get('value', 'Não Identificado')}")
        
        time.sleep(4)
        return

    def control_menu(self, menu):
        for key in menu.keys():
            print (key, '--', menu[key])
        
        option = ''
        
        try:
            option = int(input('Escolha uma das opções acima \n'))
        except:
            print('Opção inválida. Digite um número')

        if option == 0:
            self.modify_device_status(option)
        elif option == 1:
            self.modify_device_status(option)
        elif option == 2:
            self.modify_device_status(option)
        elif option == 3:
            self.modify_device_status(option)
        elif option == 4:
            self.modify_system_alarm_status()
        elif option == 5:
            self.modify_fire_alarm_status()
        else:
            return

    def turn_on_turn_off(self):
        print("0 - Desligar")
        print("1 - Ligar")
        result = input("Escolha uma das opções acima.\n")

        if int(result) == 0:
            return False

        elif int(result) == 1:
            return True
        else:
            print("Valor inválido")
            return -1

    def modify_device_status(self, option):
        value = self.turn_on_turn_off()
        if value != -1:
            self.outputs[option]['value'] = value
            print(option)
            print(self.outputs[option])
            send_data_to_client(self.outputs[option], self.client_data[0][1], self.client_data[0][2])

    def modify_system_alarm_status(self):
        pass

    def modify_fire_alarm_status(self):
        pass


if __name__=='__main__':
    f = open('ConfigurationFiles/initial_state.json')
    data = json.load(f)

    dist = Central(data)