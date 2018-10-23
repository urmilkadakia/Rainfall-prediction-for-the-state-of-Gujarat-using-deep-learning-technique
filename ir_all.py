import h5py
import csv
import numpy as np
import os
from PIL import Image
import statistics

# iterating through all files
path = '/home/geospacial2/PycharmProjects/BTP/IR/June_2014'
#path = '/home/geospacial2/Desktop'
file_no = 0
for subdir, dirs, files in os.walk(path):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".h5"):
            file_name = file.split('_')
            d = file_name[1]
            day = "06" + d[0:2] + d[5:]
            t = file_name[2]
            time_crop = t[0:2]
            file_no = file_no + 1
            f = h5py.File(filepath, 'r')
            heading = list(f.keys())
            # print(heading)

            # projection information and lat, long
            projection = f['Projection_Information']
            proj_attr = list(projection.attrs)
            # print(proj_attr)

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
            # print(tir1.shape[1])
            # tir1_gray = list(tir1)
            tir1_gray = tir1[0]
            tir1_gray = np.array(tir1_gray)
            # print(tir1_gray.min())
            # print(tir1_gray.shape)

            # water vapour gray count values
            wv = f['IMG_WV']
            wv_gray = wv[0]
            wv_gray = np.array(wv_gray)

            # wv radiance values
            wv_rad = f['IMG_WV_RADIANCE']
            wv_rad = list(wv_rad)

            # tir1 temp values
            tir1_temp = f['IMG_TIR1_TEMP']
            tir1_temp = list(tir1_temp)
            # print(tir1_temp)

            # creating count -> temp lookup table
            dic = {}
            for i in range(tir1_temp.__len__()):
                dic[i] = tir1_temp[i]
            # print(dic.__len__())

            # creating count -> radiance lookup table
            dic1 = {}
            for i in range(wv_rad.__len__()):
                dic1[i] = wv_rad[i]

            # storing tir1 brightness temp values
            temp = np.empty((tir1_gray.shape[0], tir1_gray.shape[1],))
            for i in range(tir1_gray.shape[0]):
                for j in range(tir1_gray.shape[1]):
                    temp[i][j] = dic[tir1_gray[i][j]]
            # print(temp)

            # storing wv radiance values
            rad = np.empty((wv_gray.shape[0], wv_gray.shape[1],))
            for i in range(wv_gray.shape[0]):
                for j in range(wv_gray.shape[1]):
                    rad[i][j] = dic[wv_gray[i][j]]

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
                    upper_left_long1 = upper_left_long1 + (upper_right_long - upper_left_long1) / tir1_gray.shape[1]
                upper_left_long1 = upper_left_long
                upper_left_lat1 = upper_left_lat1 - (upper_left_lat1 - lower_left_lat) / tir1_gray.shape[0]

                # bottom lat and right long
            for i in range(tir1_gray.shape[0]):
                upper_left_lat2 = upper_left_lat2 - (upper_left_lat2 - lower_left_lat) / tir1_gray.shape[0]
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
            # print(temperature)

                # storing radiance in a list
            radiance = []
            for i in range(wv_gray.shape[0]):
                for j in range(wv_gray.shape[1]):
                    radiance.append(rad[i][j])

                # retrieving srtm (elevation values)
            im = Image.open('/home/geospacial2/PycharmProjects/BTP/srtm_map.tif')
            # print(im.mode)
            # im.mode = 'I'
            # im.show()
            #print(im.size)

            imarray1 = np.array(im)
            #print(imarray1.shape)
            #print(imarray)

            elevation = []
            for i in range(imarray1.shape[0]):
                for j in range(imarray1.shape[1]):
                    elevation.append(imarray1[i][j])

            #elevation = np.array(elevation)
            if int(d[0:2]) < 16:
                im = Image.open(
                    '/home/geospacial2/PycharmProjects/BTP/ndvi/ocm2_ndvi_filt_01to15_jun2014_v01_01/06012014.tif')
            else:
                im = Image.open(
                    '/home/geospacial2/PycharmProjects/BTP/ndvi/ocm2_ndvi_filt_16to30_jun2014_v01_01/06162014.tif')
            # print(im.mode)
            # im.mode = 'I'
            # im.show()
            #print(im.size)

            imarray2 = np.array(im)
            #print(imarray2.shape)
            #print(imarray)

            vegetation = []
            for i in range(imarray2.shape[0]):
                for j in range(imarray2.shape[1]):
                    if imarray2[i][j] == 255 or imarray2[i][j] == 240 or imarray2[i][j] == 230:
                        vegetation.append(-9999)
                    else:
                        vegetation.append(imarray2[i][j])

            #print(vegetation)

                # storing time
            time = []
            for i in range(len(temperature)):
                time.append(time_crop)

                # storing date
            date = []
            for i in range(len(temperature)):
                date.append(day)

                # Writing to a csv file
            data = np.empty((8, len(temperature),))
            data[0] = lat1
            data[1] = lat2
            data[2] = long1
            data[3] = long2
            data[4] = temperature
            data[5] = radiance
            data[6] = date
            data[7] = time
            data = list(map(list, zip(*data)))
            #print(len(data))
            index = []

            for i in range(len(data)):
                if data[i][0] < 25.0 and data[i][1] > 20.0 and data[i][2] > 68.0 and data[i][3] < 75.0:
                    index.append(i)

            dataset = np.zeros((len(index), 14))
            count = 0
            for i in index:
                dataset[count][0] = data[i][0]
                dataset[count][1] = data[i][1]
                dataset[count][2] = data[i][2]
                dataset[count][3] = data[i][3]
                dataset[count][4] = data[i][4]
                dataset[count][5] = data[i][5]
                dataset[count][6] = data[i][6]
                dataset[count][7] = data[i][7]
                dataset[count][8] = elevation[count]
                dataset[count][9] = vegetation[count]
                count = count + 1
            #print(len(dataset))

            columns = 334
            rows = 248
            derived = np.empty((rows, columns,))
            for i in range(rows):
                for j in range(columns):
                    derived[i][j] = dataset[j + i*columns][4]

            #print(derived.shape)

                # Deriving stats of 3x3 pixel window
            index1 = [-1, 0, 1]
            temp1 = []
            mean3 = []
            std3 = []

            for i in range(derived.shape[0]):
                for j in range(derived.shape[1]):
                    for x in index1:
                        for y in index1:
                            try:
                                temp1.append(derived[i+x][j+y])
                            except IndexError:
                                continue
                    m3 = statistics.mean(temp1)
                    s3 = statistics.stdev(temp1)
                    mean3.append(m3)
                    std3.append(s3)
                    temp1.clear()

            #print(len(mean3))
            #print(mean5)

                # Deriving stats of 5x5 pixel window
            index2 = [-2, -1, 0, 1, 2]
            temp2 = []
            mean5 = []
            std5 = []

            for i in range(derived.shape[0]):
                for j in range(derived.shape[1]):
                    for x in index2:
                        for y in index2:
                            try:
                                temp2.append(derived[i + x][j + y])
                            except IndexError:
                                continue
                    m5 = statistics.mean(temp2)
                    s5 = statistics.stdev(temp2)
                    mean5.append(m5)
                    std5.append(s5)
                    temp2.clear()

            #print(len(mean5))
            #print(mean5)

            for i in range(len(elevation)):
                dataset[i][10] = mean3[i]
                dataset[i][11] = std3[i]
                dataset[i][12] = mean5[i]
                dataset[i][13] = std5[i]

            print(file_no)
            out_path = '/home/geospacial2/PycharmProjects/BTP/Output/June_2014/' + '%s/' % d[0:2]
            out_file = day + '_' + time_crop
            with open(out_path + '%s.csv' % out_file, 'w+') as f1:
            #with open("temp.csv", 'w+') as f1:
                writer = csv.writer(f1)
                writer.writerow(["Top Latitude", "Bottom Latitude", "Left Longitude", "Right Longitude",
                                 "TIR1_Temperature", "WV_Radiance", "Date", "Time", "Elevation", "Vegetation", "Mean3",
                                 "Std3", "Mean5", "Std5"])
                writer.writerows(dataset)
                f1.close()
            f.close()