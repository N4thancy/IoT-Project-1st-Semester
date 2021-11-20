from machine import Pin
# from time import sleep
import dht

dht_sensor = dht.DHT11(Pin(14))
measure_interval = 30000
measure_last_time = 0

def measure():
    dht_sensor.measure()

def get_temp():
    return str(dht_sensor.temperature())

def get_hum():
    return str(dht_sensor.humidity())

"""while True:
    measure()
    print(get_temp())
    print(get_hum())
    sleep(5) """
