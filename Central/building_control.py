import time

from comunication import send_data_to_client
from utils import correct_input
    
def building_control(obj):
    print()
    print("Tela de Controle do Prédio:")
    print("0 -- Acionar/Desligar Sistema de Alarme")
    print("1 -- Acionar/Desligar Alarme de Incêndio")
    print("2 -- Acionar Todas Lâmpadas do Prédio")
    print("3 -- Desligar Todas Cargas do Prédio")
    item_option = correct_input(0, 3)


    if item_option < 2:
        print()
        print("0 -- Desligar")
        print("1 -- Acionar")
        status_option = correct_input(0, 1)

    print()
    
    if item_option == 0:
        modify_system_alarm_status(obj, status_option)
    elif item_option == 1:
        modify_fire_alarm_status(obj, status_option)
    elif item_option == 2:
        turn_on_all_lights(obj)
    elif item_option == 3:
        turn_off_all_output_devices(obj)
        

def modify_system_alarm_status(obj, status_option):
    if status_option == 0:
        obj.alarm_system = False
        for key, value in obj.client_rooms.items():
            obj.outputs[value][4]['value'] = False
            send_data_to_client(obj.outputs[value][4], obj.client_data[value][1], obj.client_data[value][2])
            time.sleep(0.4)
        
        print("Sistema de alarme desativado")
    else:
        for key, value in obj.client_rooms.items():
            for item in obj.inputs[value]:
                if item['type'] == 'presenca' or item['type'] == 'porta' or item['type'] == 'janela':
                    if item['value'] == True:
                        print(f"O dispositivo de {item['type']} da {key} está ativo, não é possível acionar o alarme")
                        return
        
        obj.alarm_system = True
        print("Sistema de alarme ativado")


def modify_fire_alarm_status(obj, status_option):
    if status_option == 0:
        obj.fire_alarm = False
        for key, value in obj.client_rooms.items():
            obj.outputs[value][4]['value'] = False
            send_data_to_client(obj.outputs[value][4], obj.client_data[value][1], obj.client_data[value][2])
            time.sleep(0.4)
        print("Alarme de incêndio desativado")
    else:
        for key, value in obj.client_rooms.items():
            for item in obj.inputs[value]:
                if item['type'] == 'fumaca':
                    if item['value'] == True:
                        print(f"O dispositivo de {item['type']} da {key} está ativo, não é possível acionar o alarme")
                        return
        
        obj.fire_alarm = True
        print("Alarme de incêndio ativado")

def turn_off_all_output_devices(obj):
    for room_value in obj.client_rooms.values():
        for i, _ in enumerate(obj.outputs[room_value]):
            obj.outputs[room_value][i]['value'] = False
            send_data_to_client(obj.outputs[room_value][i], obj.client_data[room_value][1], obj.client_data[room_value][2])
            time.sleep(0.1)

def turn_on_all_lights(obj):
    for room_value in obj.client_rooms.values():
        for i, item in enumerate(obj.outputs[room_value]):
            if item['type'] == 'lampada':
                obj.outputs[room_value][i]['value'] = True
                send_data_to_client(obj.outputs[room_value][i], obj.client_data[room_value][1], obj.client_data[room_value][2])
                time.sleep(0.1)