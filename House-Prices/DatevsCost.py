#code to plot the house price against time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as py
from datetime import datetime
import pylab as pl

#read the csv file in
df = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Houseprice_2009_100km_London.csv', header=0)
de = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/income.csv', header = 0)


def changepricetonum(column):
    data = [] #create an empty list called data for adding the price column data into

    for row in column:    #scans each row in Price             
        data.append(row)                        #appends the row to the data list
 

    data = [w.replace('_','') for w in data]  #for each vlaue in the list replace the underscore with nothing

    #put the data back into a new column called Price1
    df['Price1'] = data
changepricetonum(df['Price'])  #call function hashtag these out if we only need one part of the code



#need to convert the date to a datetime instead of a string
def datetodatetime(column):
    date = []
    for row in column:    #scans each row in Price             
        date.append(datetime.strptime(row,"%Y-%m-%d %H:%M"))  #appends the data with the datetime from that row

    df['Date']=date   #puts it back as a datetime coluumn
datetodatetime(df['Trdate'])  #call function
   
#plot graph of time against price
def plotscatterdate(x,y):
    plt.scatter(pl.date2num(x),y)   #puts the date as a number in .date2num
    plt.xlim(733400,735400)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))  #reformat x axis to show date in correct format
    plt.ylim(0,)
    plt.xlabel('Year')
    plt.ylabel('Price in Pounds')
    plt.title('Scatter of Price against Time')
    plt.show()
plotscatterdate(df['Date'],df['Price'])
    
#plots a scatter
def plot(x,y):
    plt.plot(x,y)  
    plt.ylim(0,)
    plt.xlabel('Percentile')
    plt.ylabel('Weekly Income in Pounds')
    plt.title('Plot of Percentiles of Income')
    plt.show()
plot(de['Percentile'],de['Weeklyincome'])


#make a histogram showing the number of house sold at different pices, is it gaussian?
def plothisto(column):
    
    price = []
    for row in column:
        price.append(float(row))#they need to be floats to put into histogram
    m = py.mean(price)
    m_y = 25000
    s = py.std(price)
    plt.hist(price, bins = [i*50000 for i in range(0,50)],  color = 'red')
    plt.plot(m, m_y, 'ko')
    plt.plot([m-s,m+s], [m_y]*2, 'k-')
   
    plt.tick_params(axis='x', direction = 'out')
    plt.xlim(0,)
    plt.xlabel('Price in Pounds')
    plt.ylabel('Number of houses being sold at that price')
    plt.title('House sales 09-14: mean = %.3f, std = %.3f' %(m,s))
    plt.show()
plothisto(df['Price1']) #call function


#function to check the number of houses outside a certain number of deviations, useful for checking if gaussian
def percentnumber(column, numstd):
    price = []
    for row in column:
        price.append(float(row))
    m = py.mean(price)
    s = py.std(price)
    count = 0
    for i in price:
        if i > m + numstd*s:
            count += 1
    return count
print percentnumber(df['Price1'],4)


#function to plot the monthly averages against the date
def plotaverages(data):
    months = list(data.apply(set)[7])   #we need a list of all the uniqe months
    months1 = []
    for row in months:
        months1.append(datetime.strptime(row,"%Y-%m"))   #create a list with unique months as datetime values
    means = []
    for i in months:  #for each date in months to iterate loop below
        dd = data[data['Month'] == i]  #change the dataset to only include thos rows with unique months
        price = []
        for row in dd['Price1']:   #for each row that corresponds with that unique month
            price.append(float(row))  #add it to a list
        means.append(py.mean(price))  #then add the value to a means list, then iterate
    x = months1   #plot
    y = means
    x, y= (list(i) for i in zip(*sorted(zip(x,y))))   #to numerically order both arrays in date order, relating the individual values from each array
    plt.plot(pl.date2num(x), y)
    plt.xlim(733400,735400)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))  #reformat x axis to show date in correct format
    plt.xlabel('Date')
    plt.ylabel('Mean Price in Pounds')
    p = py.polyfit(pl.date2num(x),y,1)   #fit a straight line with order 1
    plt.plot(pl.date2num(x), p[0]*pl.date2num(x) + p[1], 'r-')  #plot x against the coeffecients ofthe line, p[0]x + p[1] == mx + c
    plt.show()
plotaverages(df)  #call function
