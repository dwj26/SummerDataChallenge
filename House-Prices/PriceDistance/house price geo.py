# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 15:16:28 2014

@author: Dan
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import cos,radians,sin,pow,asin,sqrt
from datetime import datetime

#read the csv file in
df = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Houseprice_2009_100km_London.csv', header=0)
ds = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/metro_and_railway_stations.csv',header=0)

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

def finddistances(data):  #function to find distances to London (KGX)
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

#this is a ridiculously long function, I was thinking of making it more efficient with Cython eventually, 1hour run time
def numberwithinradius(data, data1):#function to find the number of train stations within a certain radius
    latitude=[]
    for row in data['Latitude']:  
        latitude.append(float(row))   #for each latitude put it in the latitude list
    longitude = []
    for row in data['Longitude']:  #for each longitude put it in the longitude list
        longitude.append(float(row))
    latlong= []
    for elem in zip(latitude, longitude):   #for each element in latitude and longitude (dependently) add it to a list
        latlong.extend(elem)
    latitude1 = []
    for row in data1['Latitude']:
        latitude1.append(float(row))
    longitude1=[]
    for row in data1['Longitude']:
        longitude1.append(float(row))
    latlong1 = []
    for elem in zip(latitude1, longitude1):   #for each element in latitude and longitude (dependently) add it to a list
        latlong1.extend(elem)
    number = []
    start = datetime.now()
    for e,f in zip(latlong,latlong[1:])[::2]:  #for each latitude and longitude in the housing list
        count = 0
        for c,d in zip(latlong1,latlong1[1:])[::2]:  #and for each latitude and longitude in the railway list
            radius = 6371 # radius of the earth in km, roughly https://en.wikipedia.org/wiki/Earth_radius

            # Lat,long are in degrees but we need radians
            lat1 = radians(e)
            lat2 = radians(c)
            long1 = radians(f)
            long2 = radians(d)

            dlat = lat2-lat1
            dlon = long2-long1

            a = pow(sin(dlat/2),2) + cos(lat1)*cos(lat2)*pow(sin(dlon/2),2)
            distance = 2 * radius * asin(sqrt(a))

            if distance <= 1:  #calculate the distance
                count +=1    #add one to the coun if distance less than a km, then go back and loop for each railway
        number.append(count)  #append the count of the number of railways to the number list and loop for each house
    end = datetime.now()
    print end - start    #code to time the operation, theis takes about 1hour 10 minutes! More efficient with Cython
    data['Number'] = number  #put this into the date column
numberwithinradius(df, ds)  #call the function



def findintegerdistancesandmean(data):   #a function to plot median prices of houses at certain integer distances (0-103km) from London
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
        median.append(np.median(price)) #at the median of all those at this km to a list called medians, repeat
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
    plt.xlim(0,)
    plt.xlabel('Number of Railways')
    plt.ylabel('Price in Pounds')
    plt.title('Scatter of Price against Number of Railways')
    plt.show()
plotscatterdate(df['Number'],df['Price1'])  

#this code can take a long time to run, so an email notification is set up to email when the code is complete

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

msg = MIMEMultipart()
msg['From'] = 'd.w.j"live.co.uk'
msg['To'] = 'dwj26@cam.ac.uk'
msg['Subject'] = 'Code update'
message = 'Code has finsihed running at '+ str(datetime.now())
msg.attach(MIMEText(message))

mailserver = smtplib.SMTP('smtp.live.com',587)
# identify ourselves to smtp live client
mailserver.ehlo()
# secure our email with tls encryption
mailserver.starttls()
# re-identify ourselves as an encrypted connection
mailserver.ehlo()
mailserver.login('d.w.j@live.co.uk', '**************')

mailserver.sendmail('d.w.j@live.co.uk','dwj26@cam.ac.uk',msg.as_string())

mailserver.quit()
