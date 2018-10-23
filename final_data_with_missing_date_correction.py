import pandas as pd
from dateutil.parser import parse
import csv

df = pd.read_csv('final_rain_2014.csv')

print(df.loc[0])
missing = list()

for i in range(1, len(df)):
    today = parse(df.loc[i][4])
    prev = parse(df.loc[i-1][4])
    # checking station
    if df.loc[i][0] == df.loc[i-1][0]:
        # month of present and previous record is same or not
        if today.month == prev.month:
            # date of present and previous record is same or not
            if int(today.day) == int(prev.day):
                # time of present and previous record is same or not
                if int(df.loc[i][3]) - int(df.loc[i-1][3]) > 1:
                    missing.append(i)
                    #print(df.loc[i])
            else:
                # checking whether change in date due to 24 hour cycle
                if int(df.loc[i][3]) == 0 and int(df.loc[i-1][3]) == 23:
                    continue
                else:
                    missing.append(i)
                    #print(df.loc[i])
        else:
            # Given month has 31 days or not
            if int(prev.month) == 7 or int(prev.month) == 8:
                # checking change in month due to completion of month or not
                if int(today.day) == 1 and int(prev.day) == 31:
                    # checking whether change in date due to 24 hour cycle
                    if int(df.loc[i][3]) == 0 and int(df.loc[i - 1][3]) == 23:
                        continue
                    else:
                        missing.append(i)
                        #print(df.loc[i])
                else:
                    missing.append(i)
                    #print(df.loc[i])
            else:
                # checking change in month due to completion of month or not
                if int(today.day) == 1 and int(prev.day) == 30:
                    # checking whether change in date due to 24 hour cycle
                    if int(df.loc[i][3]) == 0 and int(df.loc[i - 1][3]) == 23:
                        continue
                    else:
                        missing.append(i)
                        #print(df.loc[i])
                else:
                    missing.append(i)
                    #print(df.loc[i])

file_out = csv.writer(open('RAIN.csv','w+'))
file_out.writerow(['@STATION_ID', 'LATITUDE', 'LONGITUDE', 'TIME(GMT)', 'DATE(GMT)', 'RAIN_FALL(mm)'])
temp = list()
for i in range(len(df)):
    # storing data entry that are correct if there is any gap in between we are leaving not including it
    if i not in missing:
        temp = [df.loc[i][0], df.loc[i][1], df.loc[i][2], df.loc[i][3], df.loc[i][4], df.loc[i][5]]
        file_out.writerow(temp)











