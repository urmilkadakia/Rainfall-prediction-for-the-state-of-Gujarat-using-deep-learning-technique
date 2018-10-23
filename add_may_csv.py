#code to add 31st may before every new station entry

import csv

flag = 0
station = 'ISRO0009_15F009(PRL..Ahmedabad)'

# output file
file_out = csv.writer(open('output1.csv','w'))
file_out.writerow(['@STATION_ID', 'LATITUDE', 'LONGITUDE', 'TIME(GMT)', 'DATE(GMT)', 'RAIN_FALL(mm)'])
# reading file
with open('GUJARAT_ALL_31-05-2015_30-09-2015_Feb18_125894.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)
    for row in reader:

        if station != row[0]:
            flag = 0
	# cheking for last entry on 31st may
        if row[3] == '23' and row[4] == '05/31/2015':
            station = row[0]
            flag = 1
	# adding 31st may as the first entry to all the staions data
        if flag == 1:
            file_out.writerow(row)













