'''
Take a quick look at the data
Columns: Temperature, Humidity, Wind speed, Wind Direction, Gas, pm10, pm2.5, Time
'''

import glob
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_files():
    f = glob.glob('./data/*.txt')
    return f

def get_data(files):
    data = []
    f = open(files,'r')
    for line in f:
        temp = line.split(',')[0]
        data.append(temp)
    f.close()
    return data

if __name__=="__main__":

    files = get_files()    
    #data = get_data(files[1])
    #print data
    T,H,WS,WD,G,PM10,PM25,Time = np.loadtxt(files[0],delimiter=',',unpack=True)
    '''
    HT = []
    for i in range(0,len(Time)):
        human_time = dt.datetime.fromtimestamp(Time[i]).strftime('%Y-%m-%d %H:%M:%S')
        #human_time = dt.datetime.fromtimestamp(Time[i]).strftime('%Y,%m,%d,%H,%M,%S')
        HT.append(human_time)
    '''
    

    dates = [dt.datetime.fromtimestamp(ts) for ts in Time]

    ax = plt.gca()
    #xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
    xfmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=25)
    plt.plot(dates,T)
    plt.title('Temperature')
    plt.ylabel('Temperature in degrees C')
    plt.show()

    ax = plt.gca()
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=25)
    plt.plot(dates,H)
    plt.title('Humidity')
    plt.ylabel('Humidity (%)')
    plt.show()

    ax = plt.gca()
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=25)
    plt.plot(dates,WS)
    plt.title('Wind Speed')
    plt.ylabel('Wind Speed (m/s?)')
    plt.show()

    
    ax = plt.gca()
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=25)
    plt.plot(dates,WD)
    plt.title('Wind Direction')
    plt.ylabel('Wind Direction')
    plt.show()


    ax = plt.gca()
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=25)
    plt.plot(dates,G)
    plt.title('Gas')
    plt.ylabel('Gas')
    plt.show()

    
    ax = plt.gca()
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=25)
    plt.plot(dates,PM10)
    plt.title('PM10')
    plt.ylabel('PM10')
    plt.show()

    ax = plt.gca()
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=25)
    plt.plot(dates,PM25)
    plt.title('PM25')
    plt.ylabel('PM25')
    plt.show()
