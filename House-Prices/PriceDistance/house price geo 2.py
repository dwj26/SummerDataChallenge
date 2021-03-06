# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 16:58:15 2014

@author: Dan
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import scipy.interpolate
import pandas as pd
import numpy as np
from datetime import datetime
import pylab as pl



df = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Houseprice_2009_100km_London.csv', header=0)
dg = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/NPSL_London100km.csv', header=0)
#function for changing the underscored price values to numbers
def sortdata(column, replace, new):
    data = [] #create an empty list called data for adding the price column data into

    for row in column:    #scans each row in Price             
        data.append(row)  #appends the row to the data list
 

    data = [w.replace(replace,'') for w in data]  #for each value in the list replace the underscore with nothing

    #put the data back into a new column called whatever is called as 'new' in the function
    df[new] = data  
    
sortdata(df['Price'], '_', 'Price1')
sortdata(df['Postcode'], ' ', 'Postcode1')  #call function, hashtag these out if we only need one part of the code

def sortpostcode(column):
    postcode = []  #create postcode list
    for i in column:  #for an element in the postocde column
        postcode.append(i[0:2])  #append the first two letters of that area
    df['AreaCode']= postcode  #put into new column call area code, area code now means the first two letters of the postcode
sortpostcode(df['Postcode1']) #call the function
                       

#need to convert the date to a datetime instead of a string
def datetodatetime(column):
    date = []
    for row in column:    #scans each row in Price             
        date.append(datetime.strptime(row,"%Y-%m-%d %H:%M"))  #appends the data with the datetime from that row use  %Y-%m-%d (%H:%M)

    df['Date']=date   #puts it back as a datetime coluumn either df['Date'] or dc['Date']
datetodatetime(df['Trdate'])  #call function with either df['Trdate'] or dc['Date']

def uniquepostcode(data,maxi):  #function to plot maps that show the gradient of increase in house prices, data = data, maxi = changing the color scale on the map to better represent the lower gradients (otherwise everythings blue)
    uniquelist = list(data.apply(set)[15])  #make a list of the unique post code areas (first 2 letters of post code)
    gradient = []  #make a list of the gradient of house price change
    for i in uniquelist:  #for each postocde area to iterate loop below
        dd = data[data['AreaCode'] == i]  #change the dataset to only include those rows with a particular unique postcode areas
        for j in dd:  #for the row in the new data set which only includes a single area code
            months = list(dd.apply(set)[7])   #we need a list of all the uniqe months
            months1 = []
            for row in months:
                months1.append(datetime.strptime(row,"%Y-%m"))   #create a list with unique months as datetime values
            medians = []
            for a in months:  #for each date in months to iterate loop below
                de = dd[dd['Month'] == a]  #change the dataset to only include those rows with unique months
                price = []
                for row in de['Price1']:   #for each row that corresponds with that unique month
                    price.append(float(row))  #add it to a list
                medians.append(np.median(price))  #then add the value to a median list, then repeat for next month
        x = months1   #plot
        y = medians
        x, y= (list(b) for b in zip(*sorted(zip(x,y))))   #to numerically order both arrays in date order, relating the individual values from each array
        p = np.polyfit(pl.date2num(x),y,1)   #fit a straight line with order 1
        #plt.show()  #plot x against the coeffecients ofthe line, p[0]x + p[1] == mx + c, unhasthag to see the plots (there are 69 of them)
        gradient.append(float(p[0])) #append each gradient to the lsit gradient, then repeat for next postcode area
    #prepare data to plot on graph   
    lats = []
    lons = []
    for a in uniquelist:  #for each post code area 
        count = 0   
        for i in dg['Pcd']:  #for each postcode present
            if i[0:2] == a:  #if the first two letters of that postcode equal the post code area
                lats.append(float(dg['Latitude'][count]))  #append the list with the lat and lon of that postcode
                lons.append(float(dg['Longitude'][count]))
                break   #then return for the next post code area (a)
            else:
                count += 1  #else increase the count/move down the list
    x = np.array(lons)
    y= np.array(lats)
    z = np.array(gradient)  #all data needs to be a numpy array
    
    xi,yi = np.linspace(x.min(),x.max(),500), np.linspace(y.min(),y.max(),500)   #code for the interpolation proccess between lats and lons
    xi,yi = np.meshgrid(xi,yi)   #need to create a grid of xi, yi
    print 'Coordinates of data centre'  #need to find the centre of the data to centre the amp around it
    print x.min() + ((x.max()-x.min())/2)
    print y.min() + ((y.max()-y.min())/2)
    rbf = scipy.interpolate.Rbf(x,y,z, function = 'linear')  #interpolate action as if a linear increase bewtween points
    zi = rbf(xi,yi)    
    m = Basemap(llcrnrlon=x.min(),llcrnrlat=y.min(),urcrnrlon=x.max(), urcrnrlat=y.max(), projection='lcc',resolution='h', lat_0=51.58195,lon_0=-0.236653)   #create a basemap for south east England centred on the centre of the plot, and the corners match with the corners of the underlying image of the plot
    lon = [-0.1257400, 0.11667, -1.25596,-0.97113,0.51667]  #plot city points to make map more readable
    lat = [51.5085, 52.2, 51.75222,51.45625,51.26667]   #city coordinates
    a,b = m(lon, lat)  #put into map axes coordinates
    m.plot(a, b, 'b.', markersize=1)  #plot point markers
    labels = ['London', 'Cambridge', 'Oxford','Reading','Maidstone']  #loop for plotting labels
    for label, xpt, ypt in zip(labels, a, b):
        plt.text(xpt, ypt, label)
    m.imshow(zi, vmin = z.min(), vmax = maxi, origin = 'lower',extent = [x.min(),x.max(),y.min(),y.max()])  #put the image of the heatmap plot onto the basemap (change the vmax) to change the associated color scale
    m.scatter(x,y,c=z)
    m.drawcoastlines()
    m.drawcounties()
    plt.colorbar()  #put the color bar next to the plot
    plt.title('Map of change in houseprices from 09-14')
    plt.show()
uniquepostcode(df,280) #call the function for maximum gradient values that make insightful plots
uniquepostcode(df,120)
uniquepostcode(df,80)
uniquepostcode(df,40)
uniquepostcode(df,20)
#code to plot  map of all house sales around London between 09-14 as a hexplot
# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
m = Basemap(width=500000, height = 500000, projection='lcc',
            resolution='h',lat_1=0,lat_2=10,lat_0=52,lon_0=0.)

lons = []
for i in df['Longitude']:
    lons.append(float(i))
lons = np.array(lons)
lats = []
for i in df['Latitude']:
    lats.append(float(i))
lats = np.array(lats)
bins = 30
# convert to map projection coordinates.
x, y = m(lons, lats)
# remove points outside projection limb.

fig = plt.figure(figsize=(12,5))
ax = fig.add_subplot(122)
CS = m.hexbin(x,y,gridsize=bins,cmap=plt.cm.jet)
# draw coastlines, lat/lon lines.
m.drawcoastlines()
m.drawparallels(np.arange(0,81,20))
m.drawmeridians(np.arange(-180,181,60))
m.colorbar(location="right",label="Z") # draw colorbar
plt.title('Heatmap of Number of Housesales', fontsize = 20)
