from comunication import send_data_to_client

import time
import threading

def trigger_alarm(client_rooms, client_data, outputs):
    for room_value in client_rooms.values():
        outputs[room_value][4]['value'] = True
        send_data_to_client(outputs[room_value][4], client_data[room_value][1], client_data[room_value][2])
        time.sleep(0.1)

def turn_lights_on(room, client_data, outputs):
    outputs[room][0]['value'] = True
    outputs[room][1]['value'] = True
    send_data_to_client(outputs[room][0], client_data[room][1], client_data[room][2])
    send_data_to_client(outputs[room][1], client_data[room][1], client_data[room][2])
    
    time.sleep(15)
    
    outputs[room][0]['value'] = False
    outputs[room][1]['value'] = False
    send_data_to_client(outputs[room][0], client_data[room][1], client_data[room][2])
    send_data_to_client(outputs[room][1], client_data[room][1], client_data[room][2])

def trigger_fire_alarm(data, fire_alarm, client_rooms, client_data, outputs):
    if data['type'] == 'fumaca' and fire_alarm and data['value']:
        thread_alarm = threading.Thread(target=trigger_alarm, args=(client_rooms, client_data, outputs, ))
        thread_alarm.start()

def trigger_system_alarm(data, system_alarm, client_rooms, client_data, outputs):
    if data['type'] == 'presenca' or data['type'] == 'porta' or data['type'] == 'janela':
        if system_alarm and data['value']:
            thread_alarm = threading.Thread(target=trigger_alarm, args=(client_rooms, client_data, outputs, ))
            thread_alarm.start()

def trigger_lights(data, system_alarm, room, client_data, outputs):
    if data['type'] == 'presenca' or data['type'] == 'porta' or data['type'] == 'janela':
        if (not system_alarm) and data['value']:
            thread_turn_lights_on = threading.Thread(target=turn_lights_on, args=(room, client_data, outputs, ))
            thread_turn_lights_on.start()