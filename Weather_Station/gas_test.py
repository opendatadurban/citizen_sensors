import spidev
import RPi.GPIO as GPIO
def readadc(pin):
    if ((pin > 7) or (pin < 0)):
        return -1
    r = spi.xfer2([1,(8+pin)<<4,0])
    adcout = ((r[1]&3) << 8) + r[2]
    return adcout

def readMQ135(mq135Pin):
    gas_array = []
    for i in range(10):
        mq135_reading = readadc(mq135Pin)
        gas_array.append(mq135_reading)
        print 'mq135 reading: ',mq135_reading
    return gas_array

if __name__=="__main__":
    pin = 1
    spi = spidev.SpiDev()
    spi.open(0,0)
    readMQ135(pin)
    spi.close()
    GPIO.cleanup()
