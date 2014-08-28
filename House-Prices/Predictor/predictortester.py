# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 21:36:46 2014

@author: Dan
"""

import random
import pandas as pd
import numpy as np


#These first lines make a file with a number of random lines from the house file, change and see change in accuracy
with open('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Houseprice_2009_100km_London.csv', "rb") as source:
    lines = [line for line in source]
    lines = lines[1:]
    source.close()
    
line1 = ['Price,Trdate,Postcode,Property_Type,Newbuild,Freeorlease,Year,Month,Oseast1M,Osnrth1M,Oa11,Latitude,Longitude\r\n']
random_choice = line1 + random.sample(lines, 500)  #3000 seems around the topend I can take with my computer memory, increase higher to check, but may kill python

with open('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Predictor/price.csv', "wb") as sink:
    sink.write("\n".join(random_choice))
    sink.close()
    
df = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Predictor/price.csv', header = 0)
df = df.dropna()

def sortdata(column, word, new):
    data = [] #create an empty list called data for adding the price column data into

    for row in column:    #scans each row in Price             
        data.append(str(row))  #appends the row to the data list
 

    data = [w.replace(word,'') for w in data]  #for each value in the list replace the underscore with nothing

    #put the data back into a new column called whatever is called as 'new' in the function
    df[new] = data  
    
sortdata(df['Price'], '_', 'Price1')

prices = []
for row in df['Price1']:
    prices.append(float(row))

df = df.drop(['Price','Price1'], axis =1)    #drop the price data as this is going to be the test data (price needs to be guessed)

header = ["Trdate", "Postcode", "Property_Type", "Newbuild", "Freeorlease","Year","Month","Oseast1M","Osnrth1M","Oa11","Latitude","Longitude"]
df.to_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Predictor/price.csv', columns = header) #write to file with the columns on the above line


"""now the general predictor code"""

import pandas as pd
import csv
from datetime import datetime
import pylab as pl
import random

#These first lines make a file with a number of random lines from the house file, change and see change in accuracy
with open('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Houseprice_2009_100km_London.csv', "rb") as source:
    lines = [line for line in source]
    lines = lines[1:]
    source.close()
line1 = ['Price,Trdate,Postcode,Property_Type,Newbuild,Freeorlease,Year,Month,Oseast1M,Osnrth1M,Oa11,Latitude,Longitude\r\n']
random_choice = line1 + random.sample(lines, 2000)  #3000 seems around the topend I can take with my computer memory, increase higher to check, but may kill python

with open('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Predictor/trainprice.csv', "wb") as sink:
    sink.write("\n".join(random_choice))
    sink.close()
    
#the first process is with the training data, trainprice, this has the price visible
df = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Predictor/trainprice.csv', header = 0)
df = df.dropna()

def sortdata(column, word, new):
    data = [] #create an empty list called data for adding the price column data into

    for row in column:    #scans each row in Price             
        data.append(str(row))  #appends the row to the data list
 

    data = [w.replace(word,'') for w in data]  #for each value in the list replace the underscore with nothing

    #put the data back into a new column called whatever is called as 'new' in the function
    df[new] = data  
    
sortdata(df['Price'], '_', 'Price1')
sortdata(df['Postcode'], ' ', 'Postcode1')  #call function, hashtag these out if we only need one part of the code
#change data to numbers as a predictor will only work with numbers
def numberprice(column):  #function to change the price from a string to a number
    price = []   #create an empty price list
    for i in column:  #for i in the dataset column
        price.append(int(i))  #append the empty list with i as an integer
    df['Cost']=price  #put back into dataset
numberprice(df['Price1'])  #call function

df['Lat'] = df['Latitude']
df['Lon']=df['Longitude']
df['Hold'] = df['Freeorlease'].map({'F':0,'L':1}).astype(int) #map Freehold to 0 and Leasehold to 1
df['Build'] = df['Newbuild'].map({'N':0,'Y':1}).astype(int) #map newbuilt to 1 and old build to 0
df['PropType']=df['Property_Type'].map({'D':0,'S':1,'T':2,'F':3}).astype(int)  #map detached to 0, semi-detached to 1, terraced to 2, flat or maisonette to 3
df = df.drop(['Year', 'Month', 'Oseast1M','Osnrth1M','Oa11', 'Longitude', 'Latitude'], axis = 1)  #delete the unused columns (some of these may be useful in future)
df = df.dropna()  #just in case, drop the NaN's


def datetodatetime(column):
    date = []
    date2 = []
    for row in column:    #scans each row in Price             
        date.append(datetime.strptime(row,"%Y-%m-%d %H:%M"))  #appends the data with the datetime from that row use  %Y-%m-%d (%H:%M)
    for i in date:
        date2.append(pl.date2num(i))
    df['Date']=date2   #puts it back as a datetime coluumn either df['Date'] or dc['Date']
datetodatetime(df['Trdate']) #call function


def sortpostcode(column):
    postcode = []  #create postcode list
    for i in column:  #for an element in the postocde column
        postcode.append(i[0:2])#append the first two letters of that area
    df['AreaCode']= postcode  #put into new column call area code, area code now means the first two letters of the postcode
    uniquelist = list(df.apply(set)[15])  #make a list of the unique post code areas (first 2 letters of post code)
    areacodenum = []  #create an empty list for the number associated with the area code to placed in (to make it predictor friendly)
    for i in df['AreaCode']:  #for each element in the AreaCode (2 letter) list
        count = 0  #start the count at 0
        for j in uniquelist:  #then search for the elements in the uniquelist (69 total)
            if i ==j:  #if the AreaCode equals that found in the unique list of areacodes
                areacodenum.append(count)  #append the count to the list
            else:
                count += 1  #else increment the count, this allows each areacode (2 letters) to have a number
    df['AreaCodeNum']=areacodenum  #put the areacode data back into the the dataset as a number
sortpostcode(df['Postcode1']) #call the function




df = df.drop(['AreaCode','Postcode1','Newbuild','Property_Type','Postcode', 'Trdate','Freeorlease','Price','Price1'], axis = 1)  #delete any of the data in the dataset that is not a number
df= df.drop(['AreaCodeNum', 'Hold', 'Date'], axis = 1)
train_data = df.values

##REPEAT the process with the test data, this is the data without the price. In this case, just one house where a price is needed.

de = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Predictor/price.csv', header = 0)
dg = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Houseprice_2009_100km_London.csv', header = 0)
de = de.dropna()
dg = dg.dropna()
def sortdata(column, replace, new,datum):
    data = [] #create an empty list called data for adding the price column data into

    for row in column:    #scans each row in Price             
        data.append(row)  #appends the row to the data list
 

    data = [w.replace(replace,'') for w in data]  #for each value in the list replace the underscore with nothing

    #put the data back into a new column called whatever is called as 'new' in the function
    datum[new] = data  
    
sortdata(de['Postcode'], ' ', 'Postcode1',de)  #call function, hashtag these out if we only need one part of the code
sortdata(dg['Postcode'], ' ', 'Postcode1',dg)
#change data to numbers as a predictor will only work with numbers
de['Lat'] = de['Latitude']
de['Lon']=de['Longitude']
de['Hold'] = de['Freeorlease'].map({'F':0,'L':1}).astype(int) #map Freehold to 0 and Leasehold to 1
de['Build'] = de['Newbuild'].map({'N':0,'Y':1}).astype(int) #map newbuilt to 1 and old build to 0
de['PropType']=de['Property_Type'].map({'D':0,'S':1,'T':2,'F':3}).astype(int)  #map detached to 0, semi-detached to 1, terraced to 2, flat or maisonette to 3
de = de.drop(['Year', 'Month', 'Oseast1M','Osnrth1M','Oa11','Latitude','Longitude'], axis = 1)  #delete the unused columns (some of these may be useful in future)
de = de.dropna()  #just in case, drop the NaN's

def datetodatetime(column):
    date = []
    date2 = []
    for row in column:    #scans each row in Price             
        date.append(datetime.strptime(row,"%Y-%m-%d %H:%M"))  #appends the data with the datetime from that row use  %Y-%m-%d (%H:%M)
    for i in date:
        date2.append(pl.date2num(i))
    de['Date']=date2   #puts it back as a datetime coluumn either df['Date'] or dc['Date']
datetodatetime(de['Trdate']) #call function


def sortpostcode(column):
    postcode1 = []  #create postcode list
    for i in dg[column]:  #for an element in the postocde column
        postcode1.append(i[0:2])#append the first two letters of that area  #put into new column call area code, area code now means the first two letters of the postcode
    uniquelist  = list(set(postcode1))   #make a list of the unique post code areas (first 2 letters of post code)
    postcode2 = []  #create postcode list
    for i in de[column]:  #for an element in the postocde column
        postcode2.append(i[0:2])#append the first two letters of that area 
    areacodenum = []#put into new column call area code, area code now means the first two letters of the postcode
    for i in postcode2:  #for each element in the AreaCode (2 letter) list
        count = 0  #start the count at 0
        for j in uniquelist:  #then search for the elements in the uniquelist (69 total)
            if i ==j:  #if the AreaCode equals that found in the unique list of areacodes
                areacodenum.append(count)  #append the count to the list
            else:
                count += 1  #else increment the count, this allows each areacode (2 letters) to have a number
    de['AreaCodeNum']=areacodenum  #put the areacode data back into the the dataset as a number
sortpostcode('Postcode1') #call the function

de = de.drop(['Postcode1','Newbuild','Property_Type','Postcode', 'Trdate','Freeorlease', 'Unnamed: 0'], axis = 1)  #delete any of the data in the dataset that is not a number
de = de.drop(['AreaCodeNum', 'Hold', 'Date'], axis = 1)
#create a numpy array

test_data = de.values

##NOW CONTINUE, this is the prediction phase

# Import the random forest package
from sklearn.ensemble import RandomForestClassifier 

# Create the random forest object which will include all the parameters
# for the fit
forest = RandomForestClassifier(n_estimators = 100)

# Fit the training data to the Survived labels and create the decision trees
forest = forest.fit(train_data[0::,1::],train_data[0::,0])


# Take the same decision trees and run it on the test data
output = forest.predict(test_data)
#need to be integers for kaggle to work
output = output.astype(float)
#need to convert array to a list to add the titles back in
output = output.tolist()
output = ['Price']+output

##TURN BACK INTO CSV FILE 


# open a file for writing.
csv_out = open('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Predictor/results.csv', 'wb')

# create the csv writer object.
mywriter = csv.writer(csv_out)

# writerow - one row of data at a time.
for row in zip(output):
    mywriter.writerow(row)

# always make sure that you close the file.
# otherwise you might find that it is empty.
csv_out.close()


"""now to find the percentage correct"""

dataset = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Predictor/results.csv', header = 0) #read in he results to a pandas dataset

results = []  #create an empty results list
for row in dataset['Price']:  #for each row in the price column
    results.append(float(row))  #append that row to the resulst list

zipped = []  #create an empty zipped list
for elem in zip(prices, results):   #for each element in prices and results (dependently) add it to a list
    zipped.extend(elem)

percentages = []  #create an empty list to store the percentage errors
for e,f in zip(zipped,zipped[1:])[::2]:  #for each item pairwise in the zipped list (prices then results)
    percentages.append(abs(((e-f)/e)*100))  #append the percentage error 

print np.median(percentages)  #print the median percentage error

#minimise the above error by playing around with the columns
#without combining column information the lowest I can get it is 26%
    
    
    
