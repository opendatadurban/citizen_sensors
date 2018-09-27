# Simple example of reading the MCP3008 analog input channels and printing


import time
import sys

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
an_chan = 1 # channel 8 (numbered 0-7)

# choose GPIO pin
ledPin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin,GPIO.OUT)

samplingTime = 280.0
deltaTime = 40.0
sleepTime = 9680.0


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
        #dustDensity = 0.17*calcVoltage-0.1

        #if dustDensity < 0:
        #    dustDensity = 0.00
            
        # Print the ADC values.
        print "Raw signal value (0 - 1023): ", voMeasured
        print "Voltage: ", calcVoltage
        #print "Dust Density: ", dustDensity
    
        time.sleep(1)
    

except KeyboardInterrupt:
    GPIO.cleanup()


