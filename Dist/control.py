import RPi.GPIO as GPIO

def control_output_devices(device):
    if device['value'] == 1:
        GPIO.output(device['gpio'],GPIO.HIGH)
    else:
        GPIO.output(device['gpio'],GPIO.LOW)

