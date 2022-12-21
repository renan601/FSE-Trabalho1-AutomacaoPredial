import RPi.GPIO as GPIO
import time
import threading

def control_output_devices(device):
    if device['value'] == 1:
        GPIO.output(device['gpio'],GPIO.HIGH)
        return True
    elif device['value'] == 0:
        GPIO.output(device['gpio'],GPIO.LOW)
        return True

def listen_to_inputs(com_socket, dist):
    time.sleep(2.5)
    for item in dist.inputs:
        item['value'] = GPIO.input(item['gpio'])
        time.sleep(0.6)
        if item['type'] != "contagem":
            thread_send = threading.Thread(target=dist.pub_to_central, args=(com_socket, item))
            thread_send.start()
    
    time.sleep(0.5)
    
    while True:
        for item in dist.inputs:
            if GPIO.input(item['gpio']) != item['value']:
                item['value'] = GPIO.input(item['gpio'])
                
                if item['tag'] == "Sensor de Contagem de Pessoas Entrada" and item['value'] == True:
                    dist.total_people += 1
                    print(dist.total_people)

                elif item['tag'] == "Sensor de Contagem de Pessoas Saída" and item['value'] == True:
                    if dist.total_people > 0:
                        dist.total_people -= 1
                        print(dist.total_people)
                else:
                    thread_send = threading.Thread(target=dist.pub_to_central, args=(com_socket, item))
                    thread_send.start()
        
        time.sleep(0.1)

