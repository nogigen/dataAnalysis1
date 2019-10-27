import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat
# type %matplotlib qt  to the console

def get_data():
    df = pd.ExcelFile("Dataset - 1.xlsx") # load the excel
    df = df.parse('4567') # getting the 2nd sheet.
    
   
    values = df['fullness_rate (%)'] # parallel list's.
    values = list(values)
    dates = df['record_date']
    dates = list(dates)
    
    # this handles the bad datas    
    i = 0
    while i < len(values) :
        if values[i] < 0.0:
            values.pop(i)
            dates.pop(i)
            i = i - 1 #decrement the index
        i = i + 1
            
    
    
    # lists which contains the datas needed.
    std = [0] * 24
    mean = [0] * 24
    cv = [0] * 24
    data_grouped_hourly = [[0], [0] , [0] , [0] , [0] , [0] , [0] , [0] , [0]
                            , [0] , [0] , [0] , [0] , [0] , [0] , [0] , [0] 
                            , [0] , [0] , [0] , [0] , [0] , [0] , [0]]
    avg_fullnes_rate_forHours = [0] * 24            # 24 elements, 1 for each hour
    avg_fullnes_rate_forHours_counter = [0] * 24     # parallel , counter list
    
    
    # creating number of rows as the number of days and creating columns for each hour which is 24.
    alldays_allhours = []
    alldays_allhours_counter = []
    dayCounter = int(dates[-1][8:10]) - int(dates[0][8:10]) + 1 # last day - first day + 1 = day counter
    for j in range(dayCounter) :
        alldays_allhours.append([])
        alldays_allhours_counter.append([])
        for k in range(24) :
            alldays_allhours[j].append(0)
            alldays_allhours_counter[j].append(0)
    
   
    # fill this allday_allhours list and its parallel counter list. Counter list will help us to calculate mean.
    for j in range(len(values)) :
        dayIndex = int(dates[j][8:10]) - int(dates[0][8:10]) # days start with 1, list starts with 0
        
        hr = dates[j][11:13] # character 11 and 12
        mn = dates[j][14:16] # character 14 and 15
        if hr[0] == "0":            
            index = int(hr[1])
        else:
            index = int(hr)
        
        if int(mn[0])  < 3:
            index = index    
        else:
            index = index + 1
        
        index = index % 24
        
        alldays_allhours[dayIndex][index] = float(values[j])
        alldays_allhours_counter[dayIndex][index] = alldays_allhours_counter[dayIndex][index] + 1
        
    
  
    # get the mean
    for j in range(len(alldays_allhours)) :
        for k in range(len(alldays_allhours[0])):
            if alldays_allhours_counter[j][k] != 0:
                alldays_allhours[j][k] = alldays_allhours[j][k] / alldays_allhours_counter[j][k]
    
    
        
    
    for j in range(len(values)):
     
        hr = dates[j][11:13] # character 11 and 12
        mn = dates[j][14:16] # character 14 and 15
        if hr[0] == "0":            
            index = int(hr[1])
        else:
            index = int(hr)
        
        if int(mn[0])  < 3:
            index = index    
        else:
            index = index + 1
        
        index = index % 24
        
        
        data_grouped_hourly[index].append(values[j])
        
    
    
    # pop the first 0 ' s
    for j in range(len(data_grouped_hourly)):
        data_grouped_hourly[j].pop(0)
        
    
    for j in range(len(data_grouped_hourly)):
        std[j] = stat.pstdev(data_grouped_hourly[j])
        mean[j] = stat.mean(data_grouped_hourly[j])
        cv[j] = ( std[j] / mean[j] ) * 100
    
    
    # now divide the data to hours. 00:30 -- 01:30 goes to 01:00 ...
    for j in range(len(values)):
        hr = dates[j][11:13] # character 11 and 12
        mn = dates[j][14:16] # character 14 and 15
        if hr[0] == "0":            
            index = int(hr[1])
        else:
            index = int(hr)
        
        if int(mn[0])  < 3:
            index = index    
        else:
            index = index + 1
        
        index = index % 24
        avg_fullnes_rate_forHours[index] = avg_fullnes_rate_forHours[index] + values[j] # add value to that specific hour
        avg_fullnes_rate_forHours_counter[index] = avg_fullnes_rate_forHours_counter[index] + 1 # increment the counter
    
    
    
    
    # get the average for each hour.
    for k in range(len(avg_fullnes_rate_forHours)):
        avg_fullnes_rate_forHours[k] = avg_fullnes_rate_forHours[k] / avg_fullnes_rate_forHours_counter[k]
    
    
    avg_fullness_rage_hours_pct_change = [0] * 24
    for j in range(len(avg_fullnes_rate_forHours)):
        if j != 23:
            avg_fullness_rage_hours_pct_change[j] = avg_fullnes_rate_forHours[j] - (avg_fullnes_rate_forHours[j - 1] + avg_fullnes_rate_forHours[j + 1]) / 2
        
        else:
            avg_fullness_rage_hours_pct_change[j] = avg_fullnes_rate_forHours[j] - (avg_fullnes_rate_forHours[j - 1] + avg_fullnes_rate_forHours[0]) / 2
    
    
    avg_fullnes_rate_forHours.append(avg_fullnes_rate_forHours[0])
    avg_fullness_rage_hours_pct_change.append(avg_fullness_rage_hours_pct_change[0])
    
    
    return avg_fullnes_rate_forHours,avg_fullness_rage_hours_pct_change,values, mean , std , cv, alldays_allhours


# display mean and std for each hour
# =============================================================================
# time = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00",
#                "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
#                "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
# =============================================================================
# =============================================================================
# displays it to the console
# for j in range(len(mean)):
#     print(time[j] ," ---> ", "mean : ", mean[j], "\t", "std : ", std[j])
# =============================================================================


# seperate the hours 04:00-16:00 to 16:00-04:00 Since between 16:00-04:00 the fullness_rate is kind of stable. However
# between 04:00-16:00 the fullness_rate goes craaaazzzyyyyy.


# raw data
def plot_raw_data(raw_data) :
  
    plt.clf()
    plt.xlabel("Data Number")
    plt.ylabel("Fullness Rate (%)")
    axes = plt.gca()
    axes.set_xlim([0,len(raw_data)])
    plt.plot(raw_data)
    
  
 

# average fullness_rate for each hours.
def plot_hourly_average(hourly_average,x) :
    
    plt.clf()
    plt.xlabel("Hours")
    plt.ylabel("Average Fullness Rate (%)")
    axes = plt.gca()
    my_xticks = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00",
                    "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
                    "18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "24:00"]
    plt.xticks(x, my_xticks)
    axes.set_xlim([0,24])
    plt.title("Average Fullness Rate for Hours")
    plt.plot(hourly_average)
    
      

# change of fullness_rate
def plot_hourly_average_change(hourly_average_pct_change,x) :
    
    plt.clf()
    plt.xlabel("Hours")
    plt.ylabel("Change of Fullness Rate")
    plt.title("The Change of Fullness Rate Between")
    axes = plt.gca()
    my_xticks = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00",
                   "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
                    "18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "24:00"]
    plt.xticks(x, my_xticks)
    axes.set_xlim([0,24])
    plt.title("Change of Fullness Rate between Hours")
    plt.plot(hourly_average_pct_change)

 
# the bar graph of std for each hours.
def plot_std_hours(std,x) :
    
    plt.clf()
    plt.xlabel("Hours")
    plt.ylabel("STD of hours")
    axes = plt.gca()
    my_xticks = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00",
                   "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
                   "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
    plt.xticks(x, my_xticks)
    axes.set_xlim([0,23])
    index = np.arange(24)
    bar_width = 0.25
    plt.label("STD of Hours and Hours")
    plt.bar(index,std, bar_width,align='edge')
    plt.legend(['STD'])


# the bar graph of cv (coefficient of variation) for each hours.
def plot_cv_hours(cv,x) :
    
    plt.clf()
    plt.xlabel("Hours")
    plt.ylabel("CV of Hours")
    axes = plt.gca()
    my_xticks = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00",
                   "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
                   "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
    plt.xticks(x, my_xticks)
    axes.set_xlim([0,23])
    index = np.arange(24)
    bar_width = 0.25
    plt.label("CV of Hours and Hours")
    plt.bar(index,cv, bar_width,align='edge')
    plt.legend(['CV'])


def plot_16to4_days1to4(alldays_allhours) :
    # 16.00 --> 16th index, 04:00 --> 4th index
    x = np.arange(12)
    plt.clf()
    
    plt.subplot(2,2,1)
    plt.title("2018-03-09")
    plt.xlabel(" Hours (16:00 - 04:00) " )
    plt.ylabel(" Fullness Rate (%) ")
   
    my_xticks = [ "17:00","18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00", "01:00", "02:00", "03:00", "04:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(7) :
        values_specific_hours.append(alldays_allhours[0][i + 17])   
    for i in range(5):
        values_specific_hours.append(alldays_allhours[0][i])     
    plt.plot(values_specific_hours)
    
    
    plt.subplot(2,2,2)
    plt.xlabel(" Hours (16:00 - 04:00) " )
    plt.ylabel(" Fullness Rate (%)")
    plt.title("2018-03-10")
    my_xticks = [ "17:00","18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00", "01:00", "02:00", "03:00", "04:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(7) :
        values_specific_hours.append(alldays_allhours[1][i + 17])   
    for i in range(5):
        values_specific_hours.append(alldays_allhours[1][i])     
    plt.plot(values_specific_hours)
    
    plt.subplot(2,2,3)
    plt.xlabel(" Hours (16:00 - 04:00) " )
    plt.ylabel(" Fullness Rate (%) ")
    plt.title("2018-03-11")
   
    my_xticks = [ "17:00","18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00", "01:00", "02:00", "03:00", "04:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(7) :
        values_specific_hours.append(alldays_allhours[2][i + 17])   
    for i in range(5):
        values_specific_hours.append(alldays_allhours[2][i])     
    plt.plot(values_specific_hours)
    
    
    plt.subplot(2,2,4)
    plt.xlabel(" Hours (16:00 - 04:00) " )
    plt.ylabel(" Fullness Rate (%) ")
    plt.title("2018-03-12")
   
    my_xticks = [ "17:00","18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00", "01:00", "02:00", "03:00", "04:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(7) :
        values_specific_hours.append(alldays_allhours[3][i + 17])   
    for i in range(5):
        values_specific_hours.append(alldays_allhours[3][i])     
    plt.plot(values_specific_hours)


def plot_16to4_days5to8(alldays_allhours) :
    # 16.00 --> 16th index, 04:00 --> 4th index
    x = np.arange(12)
    plt.clf()
    
    plt.subplot(2,2,1)
    plt.title("2018-03-13")
    plt.xlabel(" Hours (16:00 - 04:00) " )
    plt.ylabel(" Fullness Rate (%) ")
   
    my_xticks = [ "17:00","18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00", "01:00", "02:00", "03:00", "04:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(7) :
        values_specific_hours.append(alldays_allhours[4][i + 17])   
    for i in range(5):
        values_specific_hours.append(alldays_allhours[4][i])     
    plt.plot(values_specific_hours)
    
    
    plt.subplot(2,2,2)
    plt.xlabel(" Hours (16:00 - 04:00) " )
    plt.ylabel(" Fullness Rate (%) ")
    plt.title("2018-03-14")
   
    my_xticks = [ "17:00","18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00", "01:00", "02:00", "03:00", "04:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(7) :
        values_specific_hours.append(alldays_allhours[5][i + 17])   
    for i in range(5):
        values_specific_hours.append(alldays_allhours[5][i])     
    plt.plot(values_specific_hours)
    
    plt.subplot(2,2,3)
    plt.xlabel(" Hours (16:00 - 04:00) " )
    plt.ylabel(" Fullness Rate (%) ")
    plt.title("2018-03-15")
   
    my_xticks = [ "17:00","18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00", "01:00", "02:00", "03:00", "04:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(7) :
        values_specific_hours.append(alldays_allhours[6][i + 17])   
    for i in range(5):
        values_specific_hours.append(alldays_allhours[6][i])     
    plt.plot(values_specific_hours)
    
    
    plt.subplot(2,2,4)
    plt.xlabel(" Hours (16:00 - 04:00) " )
    plt.ylabel(" Fullness Rate (%) ")
    plt.title("2018-03-16")
   
    my_xticks = [ "17:00","18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00", "01:00", "02:00", "03:00", "04:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(7) :
        values_specific_hours.append(alldays_allhours[7][i + 17])   
    for i in range(5):
        values_specific_hours.append(alldays_allhours[7][i])     
    plt.plot(values_specific_hours)


def plot_4to16_days1to4(alldays_allhours) :
    # 16.00 --> 16th index, 04:00 --> 4th index
    x = np.arange(12)
    plt.clf()
    
    plt.subplot(2,2,1)
    plt.title("2018-03-09")
    plt.xlabel(" Hours (04:00 - 16:00) " )
    plt.ylabel(" Fullness Rate (%) ")
   
    my_xticks = [ "04:00","05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(12) :
        values_specific_hours.append(alldays_allhours[0][i + 4])   
       
    plt.plot(values_specific_hours)
    
    
    plt.subplot(2,2,2)
    plt.title("2018-03-10")
    plt.xlabel(" Hours (04:00 - 16:00) " )
    plt.ylabel(" Fullness Rate (%) ")
   
    my_xticks = [ "04:00","05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(12) :
        values_specific_hours.append(alldays_allhours[1][i + 4])   
       
    plt.plot(values_specific_hours)
    
    plt.subplot(2,2,3)
    plt.title("2018-03-11")
    plt.xlabel(" Hours (04:00 - 16:00) " )
    plt.ylabel(" Fullness Rate (%) ")
   
    my_xticks = [ "04:00","05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(12) :
        values_specific_hours.append(alldays_allhours[2][i + 4])   
       
    plt.plot(values_specific_hours)
    
    
    plt.subplot(2,2,4)
    plt.title("2018-03-12")
    plt.xlabel(" Hours (04:00 - 16:00) " )
    plt.ylabel(" Fullness Rate (%) ")
   
    my_xticks = [ "04:00","05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(12) :
        values_specific_hours.append(alldays_allhours[3][i + 4])   
       
    plt.plot(values_specific_hours)
    


def plot_4to16_days5to8(alldays_allhours) :
    # 16.00 --> 16th index, 04:00 --> 4th index
    x = np.arange(12)
    plt.clf()
    
    plt.subplot(2,2,1)
    plt.title("2018-03-13")
    plt.xlabel(" Hours (04:00 - 16:00) " )
    plt.ylabel(" Fullness Rate (%) ")
   
    my_xticks = [ "04:00","05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(12) :
        values_specific_hours.append(alldays_allhours[4][i + 4])   
       
    plt.plot(values_specific_hours)
    
    
    plt.subplot(2,2,2)
    plt.title("2018-03-14")
    plt.xlabel(" Hours (04:00 - 16:00) " )
    plt.ylabel(" Fullness Rate (%) ")
   
    my_xticks = [ "04:00","05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(12) :
        values_specific_hours.append(alldays_allhours[5][i + 4])   
       
    plt.plot(values_specific_hours)
    
    plt.subplot(2,2,3)
    plt.title("2018-03-15")
    plt.xlabel(" Hours (04:00 - 16:00) " )
    plt.ylabel(" Fullness Rate (%) ")
   
    my_xticks = [ "04:00","05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(12) :
        values_specific_hours.append(alldays_allhours[6][i + 4])   
       
    plt.plot(values_specific_hours)
    
    
    plt.subplot(2,2,4)
    plt.title("2018-03-16")
    plt.xlabel(" Hours (04:00 - 16:00) " )
    plt.ylabel(" Fullness Rate (%) ")
   
    my_xticks = [ "04:00","05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
    plt.xticks(x, my_xticks)
    values_specific_hours = []
    for i in range(12) :
        values_specific_hours.append(alldays_allhours[7][i + 4])   
       
    plt.plot(values_specific_hours)
    





x = np.arange(25)
(hourly_average, hourly_average_pct_change,raw_data, mean, std , cv, alldays_allhours) = get_data()
#plot_4to16_days1to4(alldays_allhours)
#plot_4to16_days5to8(alldays_allhours)
#plot_16to4_days1to4(alldays_allhours)
#plot_16to4_days5to8(alldays_allhours)

#plot_raw_data(raw_data)
plot_hourly_average(hourly_average,x)
#plot_hourly_average_change(hourly_average_pct_change,x)
#plot_std_hours(std,x)
#plot_cv_hours(cv,x)