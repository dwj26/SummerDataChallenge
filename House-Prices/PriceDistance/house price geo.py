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
    for elem in zip(latitude, longitude):   #for each element in latitude and longitude (dependently) add it to a list i.e. the new list is [lat,lon,lat2,lon2,lat3,lon3...]
        latlong.extend(elem)

    distances = []
    for a,b in zip(latlong,latlong[1:])[::2]:     #for each pairwise latlong element from the list latlong 
        distances.append(distance(a,b,51.53066,-0.1231946))  #find the distance and then append it to the list distances
    data['Distances']=distances
finddistances(df) #call the function with a particular data set

#this is a very long function, I was thinking of making it more efficient with Cython eventually, 1hour run time due to the two for loops and the zip functions within them
def numberwithinradius(data, data1):#function to find the number of train stations within a certain radius
    latitude=[]
    for row in data['Latitude']:  
        latitude.append(float(row))   #for each latitude put it in the latitude list of the houses data
    longitude = []
    for row in data['Longitude']:  #for each longitude put it in the longitude list of the houses data
        longitude.append(float(row))
    latlong= []
    for elem in zip(latitude, longitude):   #for each element in latitude and longitude (dependently) add it to a list
        latlong.extend(elem)
    latitude1 = []
    for row in data1['Latitude']:   #for each latitude in the the train data
        latitude1.append(float(row))  #append the latitude1 list
    longitude1=[]
    for row in data1['Longitude']:  #for each longitude in the train data
        longitude1.append(float(row))  #append the longitude1 list
    latlong1 = []
    for elem in zip(latitude1, longitude1):   #for each element in latitude and longitude (dependently) add it to a list
        latlong1.extend(elem)
    number = []
    start = datetime.now()
    for e,f in zip(latlong,latlong[1:])[::2]:  #for each latitude and longitude in the housing list of latlong
        count = 0  #start a count at 0
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
            distance = 2 * radius * asin(sqrt(a))  #calculate the distance

            if distance <= 1:
                count +=1    #add one to the count if distance less than a km, then go back and loop for the next railway
        number.append(count)  #append the count of the number of railways to the number list and then go back to loop for the next house
    #the number list now gives you the number of railways with a distance of 1km from each house in the list of house sales
    end = datetime.now()
    print end - start    #code to time the operation, theis takes about 1hour 10 minutes! More efficient with Cython, just gives an idea of the time with end- start
    data['Number'] = number  #put this into the date column
numberwithinradius(df, ds)  #call the function



def findgraphforrailways(one):   #a function to plot median prices of houses at certain integer distances (0-103km) from London
    integer = []  #create a new list designed to put the integer number of railways within 1km into
    for i in one:
        integer.append(int(i))  #turn the floats into integers so only integer values
    df['Railways']=integer  #create a new railway column with the integer number of railways within 1km for each house
    uniquedist = list(df.apply(set)[15]) #find the unique number of railways
    median = []
    for i in uniquedist:  #for each unique number of railways within 1km to iterate loop below
        dd = df[df['Railways'] == i]  #change the dataset to only include those rows with unique number of railways
        price = []
        for row in dd['Price1']:   #for each row that corresponds with that unique distance
            price.append(float(row))  #add it to a list
        median.append(np.median(price)) #at the median of all those with this number of railways to a list called medians, repeat for next number of railways value
    plt.scatter(uniquedist,median)   #plot a scatter
    plt.xlim(0,)
    plt.ylim(0,)
    plt.xlabel('Number of Metro/Railway Stations')
    plt.ylabel('Price in Pounds')
    plt.title('Scatter of Price against Number of Rly Stns')
    plt.show()
findgraphforrailways(df['Number'])  #call function with either df['Distance'] or df[']
    
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
#function to send email from a live account, change mailserver if not a live account
def email(emailfrom,emailto, password):
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText

    msg = MIMEMultipart()
    msg['From'] = emailfrom
    msg['To'] = emailto
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
    mailserver.login(emailfrom, password)

    mailserver.sendmail(emailfrom,emailto,msg.as_string())

    mailserver.quit()

email('d.w.j@live.co.uk','dwj26@cam.ac.uk','*****')  #call function
