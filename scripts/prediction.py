# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 21:57:43 2019

@author: Asus
"""
import numpy as np
import pandas as pd
from pandas import datetime
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from statistics import mean
# type %matplotlib qt  to the console

df = pd.ExcelFile("Dataset - 1.xlsx") # load the excel

df = df.parse('4567') # getting the 2nd sheet.

df = df[['fullness_rate (%)','record_date']]
values = df['fullness_rate (%)'] # parallel list's.
values = list(values)
dates = df['record_date']
dates = list(dates)

# converting string dates 
for i in range(len(dates)):
    new_date = datetime.strptime(dates[i],'%Y-%m-%d %H:%M:%S+00:00')
    dates[i] = new_date

# string to datetime.
df['record_date'] = pd.DataFrame(dates)
df.set_index('record_date', inplace=True)

#ax = df.plot(title="Fullness Rate and Days" ,colormap='jet',marker='.')
#ax.set_xlabel("Days")
#ax.set_ylabel("Fullness Rate (%) ")

## converting series to stationary even though it's a small data.




# AR model
X = df.values
X[88:] = X[88:] + 0.6635

df['fullness_rate (%)'] = X
ax = df.plot(title="Fullness Rate and Days" ,colormap='jet',marker='.')
ax.set_xlabel("Days")
ax.set_ylabel("Fullness Rate (%) ")

df_diff = df.diff(periods=1) # integrated of order I, denoted by d (for diff), one of the parameters for the ARIMA model
df_diff.dropna(inplace=True) # dropping the first NaN

# plt.clf()
# plt.plot(test)
# plt.plot(predictions, color='red')
# plt.title("MA Model (Moving Average with q = 1)")
# plt.xlabel("Test Data No.")
# plt.ylabel("Fullness Rate (%) ")
# plt.legend(["Test","Prediction"])




index_for_collection = -1
k = 0
condition = True
while i < len(X) and condition :
    if k != len(X) - 1 and  X[k + 1] >= 0.99:
        index_for_collection = k
        condition = False
    else:
        k += 1

print("------------" , index_for_collection)
print(dates[index_for_collection])
        
train = X[:] #  close to %80 of the data
test = X[99:] # the rest which is close to %20 of the data

predictions = []


model_ar = AR(train)
model_ar_fit = model_ar.fit() # training my forecasting model

predictions = model_ar_fit.predict(start=286, end=310)
print(len(predictions))

# =============================================================================
# plt.clf()
# plt.plot(test)
# plt.plot(predictions, color='red')
# plt.title("AR Model (AutoRegressive) ")
# plt.xlabel("Test Data No.")
# plt.ylabel("Fullness Rate (%) ")
# plt.legend(["Test","Prediction"])
# =============================================================================




# ARIMA model, patterns are p,d,q 
# p = periods taken for autoregressive model
# d -> Integrated order, difference
# q periods in moving average model
# =============================================================================
# train = X[0:56] #  close to %80 of the data
# test = X[56:] # the rest which is close to %20 of the data
# model_arima = ARIMA(train,order=(2,1,0))
# model_arima_fit = model_arima.fit()
# 
# predictions = model_arima_fit.forecast(steps=230)[0]
# print(predictions)
# print(len(predictions))
# =============================================================================




meann = []
for i in range(len(predictions)) :
    
    meann.append( abs((predictions[i] - X[56 + i]) / predictions[i]) * 100  )

array = np.array(meann)
avg = array.mean()
print(avg)

predictionsAxis = []
for i in range(25):
    predictionsAxis.append(i + 286)
 
plt.clf()
plt.plot(train)
plt.plot(predictionsAxis, predictions, color='red')
plt.title("AR Model to predict future")
plt.xlabel(" Data No.")
plt.ylabel("Fullness Rate (%) ")
plt.legend(["Data","Prediction"])

print(predictions[12], predictions[24])

print("----------------", X[index_for_collection])

print(predictions[12]-X[index_for_collection])
print(predictions[24]-X[index_for_collection])