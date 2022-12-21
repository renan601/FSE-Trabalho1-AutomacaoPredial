import adafruit_dht
import time
import threading

def read_temp_humidity(com_socket, dist):
    dhtDevice = adafruit_dht.DHT22(18)
    while True:
        try:
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            
            print("Temp: {:.1f} C    Humidity: {}% ".format(temperature_c, humidity))
            
            time.sleep(2)
            
            dist.temperature_sensor[0]['temp'] = temperature_c
            dist.temperature_sensor[0]['humidity'] = humidity
            
            thread_send_temp = threading.Thread(target=dist.pub_to_central, args=(com_socket, dist.temperature_sensor[0]))
            thread_send_temp.start()
        
        except Exception as error:
            print(error.args[0])
            time.sleep(2)
            continue