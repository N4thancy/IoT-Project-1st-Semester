from neopixel_ring import *
import time
import mqttBotPubSub
from tempSensor import *
import gpsmain
import speaker
lib = mqttBotPubSub
"""-------------- THIS IS THE MAIN FILE -------------- """

# funktion for få Conrad til at snakke, gør koden nemmere at overskue
def talkConrad(x: str):
    lib.client.publish(topic=lib.mqtt_pub_feedname, msg=x)
    lib.m = ""

# funktion for at sende et temperatur feed til adafruit
def sendTemp(x: str):
    lib.client.publish(topic=lib.mqtt_temp_feedname, msg=x)
    lib.m = ""

# funktion for at sende et humidity feed til adafruit
def sendHum(x: str):
    lib.client.publish(topic=lib.mqtt_hum_feedname, msg=x)
    lib.m = ""

# "Loop" til at udskifte spillere ud af banen
outLoop = False
# "Loop" til at skifte spillere ind på banen
inLoop = False

while True:
    # Opdatere currentTime
    currentTime = time.ticks_ms()
    #writer NeoPixel med deres nuværende værdi
    np.write()
    try:
        """# Test om conrad kan snakke via adafruit
        if lib.m == "test":
            talkConrad("Testing...")
            talkConrad("Hello!")"""

        if lib.m == "conrad udskift spilleren":
            # Checker om der er nogle udskiftnings loops igang før den igang sætter et udskiftnings loop
            if (inLoop is False and outLoop is False):
                talkConrad("Udskifter spilleren")
                # print("Starter sekvens for Udskiftning Spilleren") # Debug
                outLoop = True # Sætter udskiftnings loopet i gang
                speaker.start_track_1()
                # talkConrad("Playing Track 1")

            elif outLoop is True: # Checker om spiller er ved at blive skiftet ind
                talkConrad("Spiller er allerede ved at blive udskiftet")
            # Hvis spiller er ved at blive skiftet ind fortæller Conrad det

            elif inLoop is True: # Checker om spiller er ved at blive skiftet ud
                talkConrad("Spilleren er ved at blive skiftet ind")
                # print("Kan ikke udskifte spiller, spiller bliver skiftet in") # Debug

        if lib.m == "conrad skift spilleren ind":
            # Checker om der er nogle udskiftnings loops igang før den igang sætter et indskiftning loop
            if (inLoop is False and outLoop is False):
                talkConrad("Indskifter spilleren")
                # print("Starter sekvens for indskiftning af spiller") #Debug
                inLoop = True # Sætter indskiftnings loopet i gang
                speaker.start_track_2()
                talkConrad("Playing Track 2")

            elif outLoop is True: # Checker om spiller er ved at blive skiftet ind
                talkConrad("Spiller er allerede ved at blive udskiftet")
            # Hvis spiller er ved at blive skiftet ind fortæller Conrad det
            # Hvis spiller er ved at blive skiftet ud fortæller Conrad det

            elif outLoop is True: # Checker om spiller er ved at blive skiftet ud
                talkConrad("Spilleren er ved at blive udskiftet")
                # print("Kan ikke skifte spiller ind, spiller er ved at skiftes ud") # Debug

        # Kan stoppe ind og udskiftninger hvis træner ønsker det
        if lib.m == "conrad stop skift":
            talkConrad("Stopper skift")
            last_time = currentTime
            # Stopper musiken
            speaker.stop_mp3
            # Loops bliver lukket
            outLoop = False
            inLoop = False
            # Variables bliver "nulstillet"
            goes = 0
            rounds = 0
            # Alle neopixels slukkes
            led_full_stop()

        # Checker ved at tage den nuværede tid - den tid den sidst opdaterede en neopixel om vi har opnået den værdi vi har sat til at være vores interval
        if (currentTime - last_time > interval and outLoop is True):
            # Tid bliver opdateres
            last_time = currentTime
            set_red(goes) # Nuværende neopixel tændes
            set_off(goes) # NeoPixel 3 tilbage slukkes
            if goes == 11:
                goes = 0
                rounds = rounds + 1
            else:
                goes = goes +1

        if (currentTime - last_time > interval and inLoop is True):
            # Tid bliver opdateres
            last_time = currentTime
            set_green(goes) # Nuværende neopixel tændes
            set_off(goes) # NeoPixel 3 tilbage slukkes
            if goes == 11:
                goes = 0
                rounds = rounds + 1
            else:
                goes = goes +1

        # Hvis max antal af rounds er nået sluttes alle loops og pixels slukkes
        if rounds == max_rounds:
            # Tid bliver opdateres
            last_time = currentTime
            # Stopper musiken
            # speaker.stop_mp3
            # Loops bliver lukket
            outLoop = False
            inLoop = False
            # Variables bliver "nulstillet"
            goes = 0
            rounds = 0
            # Alle neopixels slukkes
            led_full_stop()

        if currentTime - gpsmain.gps_last_time > gpsmain.gps_interval:
            gpsmain.gps_last_time = currentTime
            gpsmain.gpsInfo()
            # threads.gps_capture()

        # Checking if it's time to measure the temperature and humidity
        if currentTime - measure_last_time > measure_interval:
            # Sets the last time a measurement accured to be the currentTime
            measure_last_time = currentTime
            # Makes the sensor measure the temperature and humidity
            measure()
            # Sender temperaturen via tempfeed til adafruit
            sendTemp(get_temp())
            # Sender luftfugtigheden via tempfeed til adafruit
            sendHum(get_hum())

        lib.client.check_msg()

    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        lib.client.disconnect()
        lib.sys.exit()






