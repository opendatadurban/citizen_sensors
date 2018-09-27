# Simple example of reading the MCP3008 analog input channels and printing


import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO

import spidev

class GPIOHelper:
    def __init__(self):
        self.pm10Pin = 7
        self.windPin = 3
        self.mq135Pin = 1
        self.ledPin = 18
        self.samplingTime = 280
        self.deltaTime = 40
        self.sleepTime = 9680
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
                
    # TRYING DIFFERENT APPROACH
    def readadc(self,adcnum):
        if ((adcnum > 7) or (adcnum <0)):
            return -1

        r = self.spi.xfer2([1,(8+adcnum)<<4,0])
        adcout = ((r[1]&3) << 8) + r[2]
        return adcout

    def readMQ135(self):
        gas_array = []
        for i in range(10):
            mq135_reading = self.readadc(self.mq135Pin)
            gas_array.append(mq135_reading)
            print "mq135 reading: ",mq135_reading
        return gas_array
    
    def readWindVane(self):
        wind_vane_array = []
        for i in range(100):
            wind_vane_reading = self.readadc(self.windPin)
            #print "wind reading: ", wind_vane_reading
            wind_vane_array.append(wind_vane_reading)
        return wind_vane_array
            
if __name__=="__main__":
    helper = GPIOHelper()
    while True:

        #helper.readSharpPM10Sensor()
        print 'smell gas'
        helper.readMQ135()
#        print 'checking wind...'
#        helper.readWindVane()
        time.sleep(3)

