# Simple example of reading the MCP3008 analog input channels and printing


import time
import sys
import numpy as np
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import spidev

# Software SPI configuration:
#CLK  = 18
#MISO = 23
#MOSI = 24
#CS   = 25
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Choose channel
an_chan = 3 # channel 8 (numbered 0-7)

# choose GPIO pin
ledPin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin,GPIO.OUT)

samplingTime = 280.0
deltaTime = 40.0
sleepTime = 9680.0

directions = {'N':3.84,'NNE':1.98,'NE':2.25,'ENE':0.41,'E':0.45,'ESE':0.32,'SE':0.90,'SSE':0.62,'S':1.40,'SSW':1.19,'SW':3.08,'WSW':2.93,'W':4.62,'WNW':4.04,'NW':4.78,'NNW':3.43}

directions = dict((v,k) for k,v in directions.iteritems())

d = [3.84,1.98,2.25,0.41,0.45,0.32,0.90,0.62,1.40,1.19,3.08,2.93,4.62,4.04,4.78,3.43]
sortd = np.sort(d)
#print sortd
midp = (sortd[1:]+sortd[:-1])/2
midp = np.insert(midp,0,0)
midp = np.insert(midp,len(midp),5.0)
print midp
#for i in range(0,len(sortd)):
#    print directions.get(sortd[i])


# Main program loop.
try:
    while True:
        GPIO.output(ledPin,0)
        time.sleep(samplingTime*10.0**-6)
        # The read_adc function will get the value of the specified channel
        voMeasured = mcp.read_adc(an_chan)

        time.sleep(deltaTime*10.0**-6)
        GPIO.output(ledPin,1)
        time.sleep(sleepTime*10.0**-66)

        calcVoltage = voMeasured*(5.0/1024)
        c = round(calcVoltage,2)
        print c
        for i in range(1,len(midp)-1):
            b = midp[i-1]
            en = midp[i+1]
            if c > 3.90 and c < 3.95:
                direction = 4.78
                break
            elif c > b and c < en:
                direction = sortd[i]
                break
            
        #dustDensity = 0.17*calcVoltage-0.1

        #if dustDensity < 0:
        #    dustDensity = 0.00
            
        # Print the ADC values.
        print "Raw signal value (0 - 1023): ", voMeasured
        print "Voltage: ", c, direction, directions.get(direction)
    
        #print "Dust Density: ", dustDensity
    
        time.sleep(1)
    

except KeyboardInterrupt:
    GPIO.cleanup()



