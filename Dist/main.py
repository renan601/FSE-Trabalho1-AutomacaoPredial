import RPi.GPIO as GPIO
import threading

from temperature_humidity import read_temp_humidity
from setup import setup
from control_inputs_outputs import control_output_devices, listen_to_inputs
from comunication import stablish_communication, send_data_to_central, receive_data_from_central

class Dist:
    def __init__(self, conf_file):
        self.conf_file = conf_file
        
        self.address = conf_file["ip_servidor_distribuido"]
        self.port = conf_file["porta_servidor_distribuido"]
        
        self.room_name = conf_file["nome"]
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
            status = control_output_devices(data)
            data['status'] = status
            
            thread_confirm = threading.Thread(target=self.pub_to_central, args=(com_socket, data))
            thread_confirm.start()

    def pub_to_central(self, socket, data):
        data['room_name'] = self.room_name
        data['people_in_room'] = self.total_people
        send_data_to_central(socket, data)

data = setup()

dist = Dist(data)

com_socket = stablish_communication(dist.room_name, dist.conf_file)

thread_listen = threading.Thread(target=dist.listen_to_central, args=(com_socket, ))
thread_listen.start()

thread_listen_inputs = threading.Thread(target=listen_to_inputs, args=(com_socket, dist, ))
thread_listen_inputs.start()

thread_listen_temperature = threading.Thread(target=read_temp_humidity, args=(com_socket, dist, ))
thread_listen_temperature.start()