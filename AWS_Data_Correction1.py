import csv

station = 'ISRO0009_15F009(PRL..Ahmedabad)'
AWS_Data = list()
rain = 0
prev_time = 23
err_neg = 0
err_ex = 0
err_mis = 0
time = 0
date = '05/31/2014'
# output file
file_out = csv.writer(open('rain2016.csv','w+'))
file_out.writerow(['@STATION_ID', 'LATITUDE', 'LONGITUDE', 'ALTITUDE(m)', 'TIME(GMT)', 'DATE(GMT)', 'AIR_TEMP(°C)',
                   'WIND_SPEED(m/s)', 'WIND_DIRECTION(deg)', 'ATMO_PRESSURE(hpa)', 'HUMIDITY(%)', 'RAIN_FALL(mm)', 'ERROR'])
# input file
with open('output2016.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    # skipping header row
    next(reader)
    for row in reader:
        #remove wrong data
        if float(row[11]) != 9999.9:
            AWS_Data.append(row)

# reading the last reading of 31st may as prev rain value
for i in range(len(AWS_Data)):
    if AWS_Data[i][5] == '05/31/2016':
        prev_timetime = 23
        rain = float(AWS_Data[i][11])
        continue
    temp = float(AWS_Data[i][11])
    if rain - temp > 924:
        AWS_Data[i][11] = temp + (1023 - rain)
    else:
        AWS_Data[i][11] = temp - rain
    rain = temp

    if float(AWS_Data[i][11]) < 0:
        AWS_Data[i].append('Neg')
        err_neg = err_neg + 1
    elif float(AWS_Data[i][11]) > 100:
        AWS_Data[i].append('Excess')
        err_ex = err_ex + 1
    file_out.writerow(AWS_Data[i])

print(err_neg,err_ex)



