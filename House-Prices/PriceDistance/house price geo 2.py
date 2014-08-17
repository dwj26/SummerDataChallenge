# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 16:58:15 2014

@author: Dan
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime
import pylab as pl
from matplotlib.mlab import griddata


df = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Houseprice_2009_100km_London.csv', header=0)
dg = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/NPSL_London100km.csv', header=0)
#function for changing the underscored price values to numbers
def sortdata(column, replace, new):
    data = [] #create an empty list called data for adding the price column data into

    for row in column:    #scans each row in Price             
        data.append(row)                        #appends the row to the data list
 

    data = [w.replace(replace,'') for w in data]  #for each vlaue in the list replace the underscore with nothing

    #put the data back into a new column called Price1
    df[new] = data
    
sortdata(df['Price'], '_', 'Price1')
sortdata(df['Postcode'], ' ', 'Postcode1')  #call function hashtag these out if we only need one part of the code

def sortpostcode(column):
    postcode = []
    for i in column:
        postcode.append(i[0:2])
    df['AreaCode']= postcode
sortpostcode(df['Postcode1'])
                       

#need to convert the date to a datetime instead of a string
def datetodatetime(column):
    date = []
    for row in column:    #scans each row in Price             
        date.append(datetime.strptime(row,"%Y-%m-%d %H:%M"))  #appends the data with the datetime from that row use  %Y-%m-%d (%H:%M)

    df['Date']=date   #puts it back as a datetime coluumn either df['Date'] or dc['Date']
datetodatetime(df['Trdate'])  #call function with either df['Trdate'] or dc['Date']

def uniquepostcode(data):
    uniquelist = list(data.apply(set)[15])
    gradient = []
    for i in uniquelist:  #for each postocde area to iterate loop below
        dd = data[data['AreaCode'] == i]#change the dataset to only include thos rows with a particular unique postcode areas
        for j in dd:
            months = list(dd.apply(set)[7])   #we need a list of all the uniqe months
            months1 = []
            for row in months:
                months1.append(datetime.strptime(row,"%Y-%m"))   #create a list with unique months as datetime values
            medians = []
            for a in months:  #for each date in months to iterate loop below
                de = dd[dd['Month'] == a]  #change the dataset to only include thos rows with unique months
                price = []
                for row in de['Price1']:   #for each row that corresponds with that unique month
                    price.append(float(row))  #add it to a list
                medians.append(np.median(price))  #then add the value to a means list, then iterate
        x = months1   #plot
        y = medians
        x, y= (list(b) for b in zip(*sorted(zip(x,y))))   #to numerically order both arrays in date order, relating the individual values from each array
        p = np.polyfit(pl.date2num(x),y,1)   #fit a straight line with order 1
        #plt.show()  #plot x against the coeffecients ofthe line, p[0]x + p[1] == mx + c, unhasthag to see the plots
        gradient.append(float(p[0]))
        
    lats = []
    lons = []
    for a in uniquelist:
        count = 0
        for i in dg['Pcd']:
            if i[0:2] == a:
                lats.append(float(dg['Latitude'][count]))
                lons.append(float(dg['Longitude'][count]))
                break
            else:
                count += 1
    lons = np.array(lons)
    lats = np.array(lats)
    gradient = np.array(gradient)
    lons, lats = np.meshgrid(lons,lats)
    

    m = Basemap(width=500000, height = 500000, projection='kav7',
                    resolution=None,lat_1=0,lat_2=10,lat_0=52,lon_0=0.)
    x, y = m(lons,lats)                
    m.contourf(x,y,gradient)
    plt.show()
uniquepostcode(df)


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
