# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 16:58:15 2014

@author: Dan
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.colors
import pandas as pd
import numpy as np

df = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Houseprice_2009_100km_London.csv', header=0)
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