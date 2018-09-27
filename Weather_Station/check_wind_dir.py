# Simple example of reading the MCP3008 analog input channels and printing


import time
import sys
sys.path.insert(0, "/usr/local/lib")

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import wiringpi
import spidev
'''
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
an_chan = 7 # channel 8 (numbered 0-7)

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
        dustDensity = 0.17*calcVoltage-0.1

        #if dustDensity < 0:
        #    dustDensity = 0.00
            
        # Print the ADC values.
        print "Raw signal value (0 - 1023): ", voMeasured
        print "Voltage: ", calcVoltage
        print "Dust Density: ", dustDensity
    
        time.sleep(1)
    

except KeyboardInterrupt:
    GPIO.cleanup()

'''


'''
class GPIOHelper:
    def __init__(self):
        self.pm10Pin = 7
        self.windPin = 3
        self.mq135Pin = 1
        #self.ledPin = 18
        self.samplingTime = 280.0
        self.deltaTime = 40.0
        self.sleepTime = 9680.0
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        
        # initialize wiringpi
        wiringpi.wiringPiSetupGpio()
        #wiringpi.pinMode(self.ledPin, 1)
        #wiringpi.digitalWrite(self.ledPin, 0) # turn LED off



    # TRYING DIFFERENT APPROACH
    def readadc(self,adcnum):
        if ((adcnum > 7) or (adcnum <0)):
            return -1

        r = self.spi.xfer2([1,(8+adcnum)<<4,0])
        adcout = ((r[1]&3) << 8) + r[2]
        return adcout



    def readSharpPM10Sensor(self):
        voMeasured = 0
        for i in range(10):
            wiringpi.digitalWrite(self.ledPin, 1) # turn LED on
            wiringpi.delayMicroseconds(self.samplingTime)
            wiringpi.delayMicroseconds(self.deltaTime)
            voMeasured = self.readadc(self.pm10Pin) # read dust value
            wiringpi.digitalWrite(self.ledPin, 0) # turn LED off
            wiringpi.delayMicroseconds(self.sleepTime)
            calcVoltage = voMeasured*(5.0/1024)
            dustDensity = 0.17*calcVoltage-0.1
            print "measured voltage: ",voMeasured
            print "calculated voltage: ",calcVoltage
            print "dust density: ",dustDensity

    def readMQ135(self):
        gas_array = []
        for i in range(10):
            mq135_reading = self.readadc(self.mq135Pin)
            gas_array.append(mq135_reading)
            #print "mq135 reading: ",mq135_reading
        return gas_array
    
    def readWindVane(self):
        #wind_vane_reading = self.readadc(self.windPin)
        #print "wind reading: ", wind_vane_reading
        wind_vane_array = []
        for i in range(100):
            wind_vane_reading = self.readadc(self.windPin)
            print "wind reading: ", wind_vane_reading
            wind_vane_array.append(wind_vane_reading)
        return wind_vane_array

'''
def read_analog(pinVal):
    #Hardware SPI configuration:
    SPI_PORT = 0
    SPI_DEVICE = 0
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

    # Choose GPIO pin - not actually sure if we need this, but leaving it in for meow
    ledPin = 18

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledPin,GPIO.OUT)

    samplingTime = 280.0
    deltaTime = 40.0
    sleepTime = 9680.0
    
    print 'checking wind direction every 3 seconds'
    try: 
        while True:
            GPIO.output(ledPin,0)
            time.sleep(samplingTime*10.0**-6)
            # The read_adc function will get the value of the specified channel
            voMeasured = mcp.read_adc(pinVal)
            time.sleep(samplingTime*10.0**-6)
            GPIO.output(ledPin,1)
            time.sleep(samplingTime*10.0**-6)
            calcVoltage = voMeasured*(5.0/1024)
            print "Voltage: ", calcVoltage
            time.sleep(3)

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__=="__main__":
    pinVal = 3
    read_analog(pinVal)
