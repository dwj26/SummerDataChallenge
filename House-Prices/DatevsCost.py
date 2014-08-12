#code to plot the house price against time

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pylab as pl

#read the csv file in
df = pd.read_csv('C:/Users/Dan/Desktop/Python Scripts(SPYDER)/Data/london2009-2014-house-prices/Houseprice_2009_100km_London.csv', header=0)



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
def plotscatter(x,y):
    plt.scatter(pl.date2num(x),y)   #puts the date as a number in .date2num
    plt.xlim(733400,735400)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))  #reformat x axis to show date in correct format
    plt.ylim(0,)
    plt.xlabel('Year')
    plt.ylabel('Price in Pounds')
    plt.title('Scatter of Price against Time')
    plt.show()
plotscatter(df['Date'],df['Price1'])     #call function

#make a histogram showing the number of house sold at different pices, is it gaussian?
def plothisto(column):
    
    price = []
    for row in column:
        price.append(float(row))#they need to be floats to put into histogram
    plt.hist(price, bins = [i*50000 for i in range(0,50)], normed = True, color = 'red')
    plt.xlabel('Price in Pounds')
    plt.ylabel('Probability of house being sold at that price')
    plt.title('Histogram to show ditribution of house sales 09-14')
    plt.show()
plothisto(df['Price1']) #call function
