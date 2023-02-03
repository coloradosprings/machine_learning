#!/usr/bin/env python
# coding: utf-8

# In[9]:


from yahoo_fin.stock_info import get_data
import tensorflow as tf
import datetime as dt
import pandas as pd
import numpy as np
import re


# In[10]:


tickers_dax_raw = """
ALV.DE	Allianz SE	171.84	-0.02	-0.01%	625,428
BAYN.DE	Bayer Aktiengesellschaft	52.15	0.07	+0.13%	1,500,256
ZAL.DE	Zalando SE	21.36	-0.03	-0.14%	1,250,728
HEI.DE	HeidelbergCement AG	43.48	0.08	+0.18%	560,708
BMW.DE	Bayerische Motoren Werke Aktiengesellschaft	75.25	0.18	+0.24%	764,182
BAS.DE	BASF SE	41.70	0.10	+0.24%	1,747,654
DTE.DE	Deutsche Telekom AG	18.69	-0.05	-0.27%	5,078,142
DB1.DE	Deutsche Börse AG	170.50	0.70	+0.41%	236,215
BEI.DE	Beiersdorf Aktiengesellschaft	103.15	0.50	+0.49%	274,241
ADS.DE	adidas AG	136.48	0.74	+0.55%	566,910
MRK.DE	MERCK Kommanditgesellschaft auf Aktien	166.90	1.00	+0.60%	160,383
1COV.DE	Covestro AG	30.01	0.19	+0.64%	1,016,604
VOW3.DE	Volkswagen AG	147.94	1.04	+0.71%	1,217,124
DTG.DE	Daimler Truck Holding AG	25.18	0.19	+0.78%	1,169,243
FME.DE	Fresenius Medical Care AG & Co. KGaA	31.46	-0.26	-0.82%	465,585
SHL.DE	Siemens Healthineers AG	43.53	-0.43	-0.98%	844,262
CON.DE	Continental Aktiengesellschaft	54.82	-0.66	-1.19%	418,691
RWE.DE	RWE Aktiengesellschaft	41.00	0.57	+1.41%	1,457,776
SIE.DE	Siemens Aktiengesellschaft	100.90	1.53	+1.54%	1,576,010
AIR.DE	Airbus SE	93.44	1.61	+1.75%	292,046
DBK.DE	Deutsche Bank Aktiengesellschaft	8.82	-0.16	-1.81%	9,398,940
LIN.DE	Linde plc	286.90	5.15	+1.83%	467,351
DPW.DE	Deutsche Post AG	32.49	-0.62	-1.89%	3,442,021
MTX.DE	MTU Aero Engines AG	157.70	3.00	+1.94%	209,342
HNR1.DE	Hannover Rück SE	159.55	3.10	+1.98%	141,850
FRE.DE	Fresenius SE & Co. KGaA	23.37	-0.53	-2.22%	1,332,040
SY1.DE	Symrise AG	102.40	2.40	+2.40%	351,967
PUM.DE	PUMA SE	57.06	1.38	+2.48%	456,639
IFX.DE	Infineon Technologies AG	24.90	0.64	+2.62%	3,570,192
HFG.DE	HelloFresh SE	23.98	-0.75	-3.03%	1,105,981
"""


# In[11]:


tickers = re.findall(fr'\w*\.DE\b',tickers_dax_raw)


# In[12]:


###collecting
class GetData_DAX:
    def __init__(self,number):
        self.number = number
        dates_x = self.get_dt((number + 1))
        dates_y = self.get_dt(number)
        self.data_x = self.collect_data_x(dates_x)
        self.data_y = self.collect_data_y(dates_y)

    def get_dt(slef,number):
        days = []
        x = 1
        for k in range(0,number):
            weekday = (dt.datetime.today().date() - dt.timedelta(days=x)).weekday()
            if weekday > 4:
                difference = 7 - weekday
                x += difference
                weekday = (dt.datetime.today().date() - dt.timedelta(days=x)).weekday()
            if weekday <= 4:
                days.append(dt.datetime.today().date() - dt.timedelta(days=x))
            x += 1
        return days

    def collect_data_x(self,dates):
        data = []
        for i,day in enumerate(dates):
            print(f"index: {i}" )
            if i < (dates.__len__() - 1):
                day_data = []        
                for ticker in tickers:
                    ticker_data = get_data(ticker, start_date = dates[i + 1],end_date=dates[i], 
                                            index_as_date = True,interval = "1m").reset_index()[['open','high','low','close']]
                    columns = ticker_data.columns
                    for index, row in ticker_data.iterrows():
                        if index == 0:
                            previous = [row[column] for column in columns]
                        elif row.isna().any() == True:
                            for column in columns:
                                row[column] = 0
                        else:
                            current = [row[column] for column in columns]
                            for index,column in enumerate(columns):
                                row[column] = previous[index] - row[column]
                            previous = current
                    ticker_data.iloc[[0]] = 0
                    ticker_data = ticker_data.values
                    if ticker_data.shape[0] != 511:
                        for x in range(ticker_data.shape[0],511):
                            ticker_data = np.insert(ticker_data,1,[0,0,0,0],0)            
                    day_data.append(ticker_data)
                data.append(day_data)
        return data


    def collect_data_y(self,dates):
        data = []
        for i,day in enumerate(dates):
            print(f"index: {i}")
            ticker = "^GDAXI"
            if i < (dates.__len__() - 1):
                    data_y = get_data(ticker, start_date = dates[i + 1],end_date=dates[i], 
                                index_as_date = True,interval = "1m")[['open']]

                    day = dates[i + 1].day if dates[i + 1].day >= 10 else f"0{dates[i + 1].day}"
                    month = dates[i + 1].month if dates[i + 1].month >= 10 else f"0{dates[i + 1].month}"
                    year = dates[i + 1].year

                    start_hour = data_y.iloc[0].name.hour
                    start_minute = data_y.iloc[0].name.minute
        
                    start_time = data_y.iloc[0].name
                    timestamp = start_time + dt.timedelta(0,0,0,0,15)
                    y_value = data_y.iloc[0] - data_y.loc[timestamp]
                    data.append(y_value)    
        return data

    # data_x = collect_data_x()
    # data_y = collect_data_y()



# In[ ]:



