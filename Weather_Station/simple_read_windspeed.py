from gpiozero import DigitalInputDevice
from time import sleep
import math


def calculate_speed(time_sec):
    global count
    radius_cm = 9.0     # Radius of the anemometer
    interval = 5        # How often to report speed
    ADJUSTMENT = 1.18   # Adjustment for weight of cups
    CM_IN_A_KM = 100000.0
    SECS_IN_AN_HOUR = 3600
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = count / 2.0

    dist_km = (circumference_cm * rotations) / CM_IN_A_KM

    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_AN_HOUR

    return km_per_hour * ADJUSTMENT

def spin():
    global count
    count = count + 1
    #print (count)
    
def get_windspeed():
    interval = 5
    inst_wind_val = calculate_speed(interval)
    return inst_wind_val


count = 0
'''
wind_speed_sensor = DigitalInputDevice(5)
wind_speed_sensor.when_activated = spin #This increases count each time the device sends a pulse. The pulse can be triggered by the slightest movement, so we should ignore if the count = 1

while True:
    count = 0
    sleep(3)
    instantaneous_windspeed = get_windspeed()
    if count == 1:
        print "wind: 0.0"
    else:
        print "wind: ",instantaneous_windspeed

'''
