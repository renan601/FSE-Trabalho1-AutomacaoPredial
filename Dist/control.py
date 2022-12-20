import RPi.GPIO as GPIO
import time

def control_output_devices(device):
    if device['value'] == 1:
        GPIO.output(device['gpio'],GPIO.HIGH)
    elif device['value'] == 0:
        GPIO.output(device['gpio'],GPIO.LOW)

