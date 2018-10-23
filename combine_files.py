import os
import csv

for i in range(31):
    if i < 9:
        st = '0' + str(i+1)
    else:
        st = str(i+1)
    os.system("cat /home/geospatial-3/Desktop/BTP/Output/August_2014/%s/08%s2014_*.csv >"
              "/media/geospatial-3/Data/Combined/August_2014/08%s2014.csv" % (st, st, st))

path = '/media/geospatial-3/Data/Combined/August_2014/'
path1 = '/media/geospatial-3/Data/Combined_1/August_2014/'

for filename in os.listdir(path):
    file_in = path + filename
    file_out = path1 + filename
    out = open(file_out, 'w+')
    file_out = csv.writer(out)
    with open(file_in, 'r') as input1:
        reader = csv.reader(input1, delimiter=',')
        # Skipping header row
        header = next(reader)
        file_out.writerow(header)
        for row in reader:
            if row[0] != 'Top Latitude':
                file_out.writerow(row)
    out.close()
