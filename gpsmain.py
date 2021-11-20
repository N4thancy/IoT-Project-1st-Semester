import GPSfunk
from machine import Pin
import mqttBotPubSub
lib = mqttBotPubSub

def map_feed(x):
    lib.client.publish(topic=lib.mqtt_map_feedname, msg=x)
    lib.m = ""

def speed_feed(x):
    lib.client.publish(topic=lib.mqtt_speed_feedname, msg=x)
    lib.m = ""

def talkConrad(x: str):
    lib.client.publish(topic=lib.mqtt_pub_feedname, msg=x)
    lib.m = ""

gps_interval = 10000
gps_last_time = 0

def gpsInfo():
    print("--------- START -------")
    gpsLatLon = GPSfunk.main()
    print("Printing GPS Data")
    # print(type(gpsLatLon))
    if gpsLatLon is not None:
        print(mapData)
        mapData = str(gpsLatLon[0])
        map_feed(mapData)
        # lib.c.publish(topic=mapFeed, msg=mapData)
        speed = str(gpsLatLon[1])
        print("Printing speed")
        print("speed: ", speed)
        speed_feed(speed)
    else:
        talkConrad("GPS has lost connection")
    print("--------- STOP -------")
    # sleep(10)

"""while True:
    gpsInfo()
    time.sleep(5)"""


