
# coding: utf-8

# # Data Import
# The choice of data was guided by Stock and Watson (1998) and obtained via the Fred api

# In[131]:

from fredapi import Fred
import pandas as pd
import numpy as np
import statsmodels.api as sm


fr = Fred(api_key='6bfc46f5628f203370685e8689fb06fb')


Y_total = fr.get_series('GDPC96') * 1000000000  #Real GDP, Billions of Dollars, Quarterly, 1929 to 2016 (Mar 30)
C_total = fr.get_series('PCECC96') * 1000000000 #Real Personal Consmuption Expenditure, Billions of Dollars, Quarterly, 1929 to 2016 (Mar 30)
I_total = fr.get_series('PNFI') * 1000000000    #Private Nonresidential Fixed Investment, Billions of Dollars, 1929 to 2016 (Mar 30)

N_index = fr.get_series('HOANBS')               #Nonfarm Business Sector: Hours of All Persons, INDEX 2009=100, Quarterly
N_2009 = fr.get_series("AWHAETP")               #Average Weekly Hours of All Employees: Total Private, Monthly

w_index = fr.get_series("COMPRNFB")             #Nonfarm Business Sector: Real Compensation Per Hour, INDEX 2009=100, Seasonally Adjusted
w_2009 = fr.get_series("CES0500000003")         #Average Hourly Earnings of All Employees: Total Private Dollars per Hour, Seasonally Adjusted

A_index = fr.get_series('OPHNFB')               #Nonfarm Business Sector: Real Output Per Hour of All Persons

i = fr.get_series('TB3MS')                      #3-Month Treasury Bill: Secondary Market Rate, Monthly
cpi = fr.get_series('CPIAUCSL')                 #Consumer Price Index for All Urban Consumers: All Items, Index 1982-1984=100, Seasonally Adjusted

pop = fr.get_series('B230RC0Q173SBEA') * 1000   #Population (midperiod), Thousands, Seasonally Adjusted Annual Rate


# # Converting Data to Correct Format
# 
# Converting all data into Quarterly time series and in the correct format for the years 1947 - 1996 (same time horizon described in King and Rebelo (2000)) 

# In[134]:



def convert_to_quarterly(df):
    df = df.groupby(pd.PeriodIndex(df.index, freq='Q'), axis=0).mean()
    return df



def convert_to_per_capita(data):
    df = pd.DataFrame(data/pop).loc['1947-01-01':'1996-10-01']
    return convert_to_quarterly(df)

Y = convert_to_per_capita(Y_total) #Real GDP per capita, Quarterly
C = convert_to_per_capita(C_total) #Real Consumption per capita, Quarterly
I = convert_to_per_capita(I_total) #Real Investment per capita, Quarterly



def convert_index_to_series(year, index):
    index_value = year.loc['2009-01-01':'2009-12-01'].mean()
    df = pd.DataFrame(index * index_value / 100).loc['1947-01-01':'1996-10-01']
    return convert_to_quarterly(df)
    
N = convert_index_to_series(N_2009,N_index).multiply(52/4) #Total per capita hours, Quarterly
w = convert_index_to_series(w_2009,w_index)                #Per capita hourly wage, Quarterly



p = cpi.pct_change().fillna(0)
r = pd.DataFrame(i/100 - p).loc['1947-01-01':'1996-12-01']      #r = i - p
r = convert_to_quarterly(r)                                     #Real interest rate, Quarterly



A = pd.DataFrame(A_index).loc['1947-01-01':'1996-10-01']
A = convert_to_quarterly(A)                                     #Real factor productivity, Quarterly



# # Table Replication

# In[135]:


table_1_data = pd.concat([np.log(pd.concat([Y, C, I, N, Y.divide(N), w, A], axis=1)), r], axis=1)
table_1_data.columns = ['Y', 'C', 'I', 'N', 'Y/N', 'w', 'A', 'r'] 


cycle, trend = sm.tsa.filters.hpfilter(table_1_data, lamb=1600)

diff = table_1_data.diff(periods=1, axis=0).fillna(0)


def table_1_replicator(data):
    first_order_autocorr = data.apply(lambda col: col.autocorr(lag=1), axis=0)
    corr = cycle.corr()["Y"]
    df = pd.concat([np.std(data), np.std(data)/np.std(data)["Y"], first_order_autocorr, corr], axis=1)
    df.columns = ["Standard Deviation", "Relative Standard Deviation", "First Order Auto-correlation", "Contemporaneous Correlation with Output"]
    return df 


# ### Table 1, HP Filtered with log values

# In[136]:

table_1 = table_1_replicator(cycle*100).round(decimals=2)
table_1


# ### Table 1, with first order difference and log values

# In[137]:

table_1_diff = table_1_replicator(diff*100).round(decimals=2)
table_1_diff


# In[ ]:




# In[ ]:



