import time

from comunication import send_data_to_client
from utils import correct_input

def room_control(obj):
    print("Deseja acionar um dispositivo em qual das salas:")
    for key, value in obj.client_rooms.items():
        print (value, '--', key)
    
    option = correct_input(0, len(obj.client_rooms)-1)
    return option

def control_menu(obj, room, menu):
    for key in menu.keys():
        print (key, '--', menu[key])
    
    print("4 -- Ligar todas as luzes da sala")
    print("5 -- Desligar todos os dispositivos da sala")
    print("6 -- Retornar ao menu principal")
    
    option = correct_input(0, 6)
    print()

    if option == 0:
        value = turn_on_turn_off()
        modify_device_status(obj, option, room, value)
    elif option == 1:
        value = turn_on_turn_off()
        modify_device_status(obj, option, room, value)
    elif option == 2:
        value = turn_on_turn_off()
        modify_device_status(obj, option, room, value)
    elif option == 3:
        value = turn_on_turn_off()
        modify_device_status(obj, option, room, value)
    elif option == 4:
        modify_device_status(obj, 0, room, True)
        modify_device_status(obj, 1, room, True)
    elif option == 5:
        modify_device_status(obj, 0, room, False)
        modify_device_status(obj, 1, room, False)
        modify_device_status(obj, 2, room, False)
        modify_device_status(obj, 3, room, False)
    elif option == 6:
        return

def turn_on_turn_off():
    print("0 - Desligar")
    print("1 - Ligar")
    result = correct_input(0, 1)
    print()
    
    if int(result) == 0:
        return False

    elif int(result) == 1:
        return True

def modify_device_status(obj, option, room, value):
    obj.outputs[room][option]['value'] = value
    send_data_to_client(obj.outputs[room][option], obj.client_data[room][1], obj.client_data[room][2])
    time.sleep(0.4)