import os, json
import socket
#import RPi.GPIO as GPIO

import logging

import threading

import time

#from control import control_output_devices
from com import stablish_communication, send_data_to_central, receive_data_from_central

class Dist:
    def __init__(self, conf_file):
        self.room_name = conf_file['nome']
        self.outputs = conf_file["outputs"]
        self.inputs = conf_file["inputs"]
        self.temperature_sensor = conf_file["sensor_temperatura"]

        #GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)

        for item in self.outputs:
            #self.setup_output_devices(item)
            item['value'] = False
            #control_output_devices(item)

    #def setup_output_devices(self, device):
        #GPIO.setup(device['gpio'],GPIO.OUT)
    
    def listen_to_central(self, com_socket):
        while True:
            data = receive_data_from_central(com_socket)
            print(data)

    #def pub_to_central(self, data):
        #send_data_to_central(data)


f = open('ConfigurationFiles/conf_sala.json')
data = json.load(f)

dist = Dist(data)

com_socket = stablish_communication(dist.room_name)

thread_listen = threading.Thread(target=dist.listen_to_central, args=(com_socket, ))
thread_listen.start()


f.close()
