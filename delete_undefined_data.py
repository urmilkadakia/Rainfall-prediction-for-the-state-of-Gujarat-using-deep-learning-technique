import csv

DATA = list()
file_out = csv.writer(open('rain2016.csv','w+'))
file_out.writerow(["Station_ID", "Latitude", 'Longitude', "Time", "Date", "Top Latitude", "Bottom Latitude",
                   "Left Longitude", "Right Longitude", "TIR1_Temperature(K)", "WV_Radiance", "Elevation(m)",
                   "Vegetation", "Mean3(K)", "Std3(K)", "Mean5(K)", "Std5(K)", "Air_Temp(°C)", "Wind_Speed(m/s)",
                   "Wind_Direction(deg)", "Atmo_Pressure(hpa)","Humidity(%)", "Rain_Fall(mm)"])

with open('final_rain2016_sorted.csv', 'r') as input1:
    reader1 = csv.reader(input1, delimiter=',')
    # Skipping header row
    next(reader1)
    for row1 in reader1:
        DATA.append(row1)

    for i in range(len(DATA)):
        DATA[i][13] = round(float(DATA[i][13]), 3)
        if float(DATA[i][12]) != -9999.0 and DATA[i][13] != -49.995:
            new_list = [DATA[i][0], DATA[i][1], DATA[i][2], DATA[i][7], DATA[i][8], DATA[i][3], DATA[i][4], DATA[i][5],
                        DATA[i][6], DATA[i][10], DATA[i][11], DATA[i][12], DATA[i][13], DATA[i][14], DATA[i][15],
                        DATA[i][16], DATA[i][17], DATA[i][18], DATA[i][19], DATA[i][20], DATA[i][21], DATA[i][22],
                        DATA[i][23]]
            file_out.writerow(new_list)

