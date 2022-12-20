import os, json
import socket
import RPi.GPIO as GPIO

import random
import threading

import time

from control import control_output_devices
from com import stablish_communication, send_data_to_central, receive_data_from_central

class Dist:
    def __init__(self, conf_file):
        self.room_name = conf_file['nome']
        self.outputs = conf_file["outputs"]
        self.inputs = conf_file["inputs"]
        self.temperature_sensor = conf_file["sensor_temperatura"]
        self.total_people = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for item in self.outputs:
            self.setup_output_devices(item)
            item['value'] = False
            control_output_devices(item)

        for item in self.inputs:
            self.setup_input_devices(item)

    def setup_output_devices(self, device):
        GPIO.setup(device['gpio'],GPIO.OUT)

    def setup_input_devices(self, device):
        GPIO.setup(device['gpio'], GPIO.IN)
    
    def listen_to_central(self, com_socket):
        while True:
            data = receive_data_from_central(com_socket)
            control_output_devices(data)
            print(data)
    
    def listen_to_inputs(self, com_socket):
        for item in self.inputs:
            GPIO.add_event_detect(item['gpio'], GPIO.RISING)
            item['value'] = GPIO.input(item['gpio'])
            thread_send = threading.Thread(target=self.pub_to_central, args=(com_socket, item))
            thread_send.start()

        while True:
            for item in self.inputs:
                if GPIO.input(item['gpio']) != item['value']:
                    item['value'] = GPIO.input(item['gpio'])
                    thread_send = threading.Thread(target=self.pub_to_central, args=(com_socket, item))
                    thread_send.start()
                    print(threading.activeCount())

            time.sleep(0.5)

    def pub_to_central(self, socket, data):
        send_data_to_central(socket, data)


f = open('ConfigurationFiles/conf_sala.json')
data = json.load(f)
f.close()

dist = Dist(data)

com_socket = stablish_communication(dist.room_name)

thread_listen = threading.Thread(target=dist.listen_to_central, args=(com_socket, ))
thread_listen.start()

thread_listen_inputs = threading.Thread(target=dist.listen_to_inputs, args=(com_socket, ))
thread_listen_inputs.start()
    
#dist.temperature_sensor[0]['value'] = random.randint(1, 40)
#send_data_to_central(com_socket, dist.temperature_sensor[0])