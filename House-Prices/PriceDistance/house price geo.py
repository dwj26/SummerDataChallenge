# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 15:16:28 2014

@author: Dan
"""

#code to plot the house price against time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as py
from datetime import datetime
import pylab as pl
from math import cos,radians,sin,pow,asin,sqrt
#read the csv file in
df = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Houseprice_2009_100km_London.csv', header=0)


#function for changing the underscored price values to numbers
def changepricetonum(column):
    data = [] #create an empty list called data for adding the price column data into

    for row in column:    #scans each row in Price             
        data.append(row)                        #appends the row to the data list
 

    data = [w.replace('_','') for w in data]  #for each vlaue in the list replace the underscore with nothing

    #put the data back into a new column called Price1
    df['Price1'] = data
changepricetonum(df['Price'])  #call function hashtag these out if we only need one part of the code


#open source code function from the internet
def distance(lat1, long1, lat2, long2):
   
    radius = 6371 # radius of the earth in km, roughly https://en.wikipedia.org/wiki/Earth_radius

    # Lat,long are in degrees but we need radians
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    long1 = radians(long1)
    long2 = radians(long2)

    dlat = lat2-lat1
    dlon = long2-long1

    a = pow(sin(dlat/2),2) + cos(lat1)*cos(lat2)*pow(sin(dlon/2),2)
    distance = 2 * radius * asin(sqrt(a))

    return distance

def finddistances(data):
    latitude=[]
    for row in data['Latitude']:  
        latitude.append(float(row))   #for each latitude put it in the latitude list
    longitude = []
    for row in data['Longitude']:  #for each longitude put it in the longitude list
        longitude.append(float(row))
    latlong= []
    for elem in zip(latitude, longitude):   #for each element in latitude and longitude (dependently) add it to a list
        latlong.extend(elem)

    distances = []
    for a,b in zip(latlong,latlong[1:])[::2]:     #for each pairwise latlong element 
        distances.append(distance(a,b,51.53066,-0.1231946))  #find the distance
    data['Distances']=distances
finddistances(df)

def findintegerdistancesandmean(data):
    integerdist = []
    for i in data['Distances']:
        integerdist.append(int(i))  #turn the floats into integers so only 0-103km integer values
    data['IntegerDistance']=integerdist
    uniquedist = list(df.apply(set)[15]) #find the unique distances
    median = []
    for i in uniquedist:  #for each distance to iterate loop below
        dd = data[data['IntegerDistance'] == i]  #change the dataset to only include thos rows with unique distances
        price = []
        for row in dd['Price1']:   #for each row that corresponds with that unique distance
            price.append(float(row))  #add it to a list
        median.append(py.median(price)) #at the median of all those at this km to a list called medians, repeat
    plt.scatter(uniquedist,median)   
    plt.xlim(0,103)
    plt.ylim(150000,)
    plt.xlabel('Distance in km')
    plt.ylabel('Price in Pounds')
    plt.title('Scatter of Price against Distance')
    plt.show()
findintegerdistancesandmean(df)
#plot graph of distance against price
def plotscatterdate(x,y):
    plt.scatter(x,y)   
    plt.xlim(0,102)
    plt.xlabel('Distance in km')
    plt.ylabel('Price in Pounds')
    plt.title('Scatter of Price against Distance')
    plt.show()
plotscatterdate(df['Distances'],df['Price1'])  



