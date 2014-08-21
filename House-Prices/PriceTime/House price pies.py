# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 17:15:53 2014

@author: Dan
"""

from pylab import *
import pandas as pd

df = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Houseprice_2009_100km_London.csv', header = 0)


def piechart(column, columnnum):
    labels = list(df.apply(set)[columnnum])
    if len(labels) == 4:
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        for i in column:
            if i == labels[0]:
                count1 += 1
            elif i == labels[1]:
                count2 += 1
            elif i == labels[2]:
                count3 += 1
            elif i == labels[3]:
                count4 += 1
            fracs = []
            fracs.append(count1)
            fracs.append(count2)
            fracs.append(count3)
            fracs.append(count4)
    elif len(labels) == 2:
        count1 = 0
        count2 = 0
        for i in column:
            if i == labels[0]:
                count1 += 1
            elif i == labels[1]:
                count2 += 1
            fracs = []
            fracs.append(count1)
            fracs.append(count2)
    pie(fracs, labels = labels)
    title('Detached, Semi-Detached, Flat or Terraced')
    show()
piechart(df['Property_Type'], 3)
    
    
        
    