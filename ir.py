import h5py
import csv
import numpy as np

f = h5py.File('/home/geospacial2/Downloads/3DIMG_15JUL2017_0130_L1C_ASIA_MER.h5', 'r')
heading = list(f.keys())
#print(heading)

# projection information and lat, long
projection = f['Projection_Information']
proj_attr = list(projection.attrs)
#print(proj_attr)

upper_left = projection.attrs.get('upper_left_lat_lon(degrees)')
upper_left_lat = upper_left[0]
upper_left_long = upper_left[1]
upper_right = projection.attrs.get('upper_right_lat_lon(degrees)')
upper_right_lat = upper_right[0]
upper_right_long = upper_right[1]
lower_left = projection.attrs.get('lower_left_lat_lon(degrees)')
lower_left_lat = lower_left[0]
lower_left_long = lower_left[1]
lower_right = projection.attrs.get('lower_right_lat_lon(degrees)')
lower_right_lat = lower_right[0]
lower_right_long = lower_right[1]

    # tir1 gray count values
tir1 = f['IMG_TIR1']
#print(tir1.shape[1])
#tir1_gray = list(tir1)
tir1_gray = tir1[0]
tir1_gray = np.array(tir1_gray)
#print(tir1_gray.min())
#print(tir1_gray.shape)

    # tir1 temp values
tir1_temp = f['IMG_TIR1_TEMP']
tir1_temp = list(tir1_temp)
#print(tir1_temp)

    # creating count -> temp look table
dic = {}
for i in range(tir1_temp.__len__()):
    dic[i] = tir1_temp[i]
#print(dic.__len__())

    # storing brightness temp values
temp = np.empty((tir1_gray.shape[0], tir1_gray.shape[1],))
for i in range(tir1_gray.shape[0]):
    for j in range(tir1_gray.shape[1]):
        temp[i][j] = dic[tir1_gray[i][j]]
#print(temp)

    # storing lat, long of each pixel
lat1 = []
lat2 = []
long1 = []
long2 = []
upper_left_long1 = upper_left_long
upper_left_long2 = upper_left_long
upper_left_lat1 = upper_left_lat
upper_left_lat2 = upper_left_lat

    # top lat and left long
for i in range(tir1_gray.shape[0]):
    for j in range(tir1_gray.shape[1]):
        lat1.append(upper_left_lat1)
        long1.append(upper_left_long1)
        upper_left_long1 = upper_left_long1 + (upper_right_long-upper_left_long1)/tir1_gray.shape[1]
    upper_left_long1 = upper_left_long
    upper_left_lat1 = upper_left_lat1 - (upper_left_lat1 - lower_left_lat)/tir1_gray.shape[0]

    # bottom lat and right long
for i in range(tir1_gray.shape[0]):
    upper_left_lat2 = upper_left_lat2 - (upper_left_lat2 - lower_left_lat)/tir1_gray.shape[0]
    for j in range(tir1_gray.shape[1]):
        upper_left_long2 = upper_left_long2 + (upper_right_long - upper_left_long2) / tir1_gray.shape[1]
        lat2.append(upper_left_lat2)
        long2.append(upper_left_long2)
    upper_left_long2 = upper_left_long

    # storing temperature in a list
temperature = []
for i in range(tir1_gray.shape[0]):
    for j in range(tir1_gray.shape[1]):
        temperature.append(temp[i][j])
#print(temperature)

    # Writing to a csv file
data = np.empty((5, len(temperature),))
data[0] = lat1
data[1] = lat2
data[2] = long1
data[3] = long2
data[4] = temperature
data = list(map(list, zip(*data)))
print(len(data))
index = []

for i in range(len(data)):
    if data[i][1] < 25.0 and data[i][0] > 20.0 and data[i][3] > 68.0 and data[i][2] < 75.0:
        index.append(i)

dataset = np.zeros((len(index), 5))
count = 0
for i in index:
    dataset[count][0] = data[i][0]
    dataset[count][1] = data[i][1]
    dataset[count][2] = data[i][2]
    dataset[count][3] = data[i][3]
    dataset[count][4] = data[i][4]
    count = count + 1
print(len(dataset))

with open('ir.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["Top Latitute", "Bottom Latitude", "Left Longitude", "Right Longitude", "Temperature"])
    writer.writerows(dataset)