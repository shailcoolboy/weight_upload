import RPi.GPIO as GPIO
import time
import sys
import thingspeak
from hx711 import HX711

# ThingSpeak keys
channel_id = "200111"
write_key  = "8ZKB7R9619BZ0CJ7"
FREQUENCY = 16 # Record data at this time interval in seconds

def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(515)
hx.reset()
hx.tare()
time.sleep(1)
channel = thingspeak.Channel(id=channel_id,write_key=write_key)

while True:
    try:
        val = hx.get_avg_weight(5, 2)
        if val<1:
             val=0.0
        try:
             response = channel.update({1:val})
        except:
             print response
             print "connection failed"

        hx.power_down()
        hx.power_up()
        time.sleep(FREQUENCY)
    except(KeyboardInterrupt, SystemExit):
        cleanAndExit()