import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sp
import os
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

ticker1 = "VG"
ticker2 = "BABA"
time_interval = '15min'
ts = TimeSeries(key='XP12DSLMVA2QP4MO', output_format='pandas')
data, meta_data = ts.get_intraday(symbol = ticker1,interval=time_interval, outputsize='full')
stock2, meta_data = ts.get_intraday(symbol= ticker2,interval=time_interval, outputsize='full')
# print(stock2.describe())
# print(data.describe())

# a = ts.keys()

#filter out values before 10am because they mess up the data
index_value = data.index
hours = int(index_value.str[11:13])
minutes = int(index_value.str[14:16])
data.ix[(hours == "09") & (30 <= minutes < 60)]

numpyStock1 = data['close'].as_matrix()
numpyStock2 = stock2['close'].as_matrix()


def convert_to_slopes(arr_vals):
    slopes = []
    prev = 0
    next = 0
    size = len(numpyStock1)
    for index in range(1, len(arr_vals) - 2, 1):
        prev = arr_vals[index - 1, 3]
        next = arr_vals[index + 1, 3]
        slope = next - prev
        if slope > 0:
            slopes.append(1)
        else:
            slopes.append(0)
    return slopes


#cost function
def calc_cost(stock1, stock2):
    cost = sp.chisquare(stock1, stock2)
    return cost

slopes1 = np.array(convert_to_slopes(numpyStock1))
slopes2 = np.array(convert_to_slopes(numpyStock2))

cost = calc_cost(slopes1, slopes2)
#gets the first 5 vals
data.head()



#gets descriptive stats
cost = 999999999999
best = None
for info in data:
    if calc_cost(stock2, info) < cost:
        best = info
        cost = calc_cost(stock2, info)






