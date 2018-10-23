import cv2
import numpy as np
import h5py

# f = h5py.File('/home/geospacial2/Downloads/3DIMG_15JUL2017_0130_L1C_ASIA_MER.h5', 'r')
# data_main = list(f.keys())
# print(data_main)
# GreyCount = f['GreyCount']
# tir1 = f['IMG_TIR1']
# print(tir1[0,0,:])
# print(tir1.shape)
# print(tir1.dtype)
#
# l1 = list(tir1)
# print(l1[0][0])
# print(list(tir1.attrs.get('resolution')))
#amv_dataset = amv.get('GeoX')
#amv_dataset = np.array(amv_dataset)
#print(amv_dataset)
#amv_dataset = amv.get('AMV_Dataset')
#amv_dataset = np.array(amv_dataset)
#print(amv_dataset)

#file = 'test.jpg'
#cv2.imwrite(file, amv_dataset[1:4])

import h5py
import csv
import numpy as np
import os
from PIL import Image

# iterating through all files

path = '/home/geospacial2/PycharmProjects/BTP/IR/June_2014'
file_no = 0
for subdir, dirs, files in os.walk(path):
    for file in files:
        try:
            filepath = subdir + os.sep + file
            if filepath.endswith(".h5"):
                file_name = file.split('_')
                d = file_name[1]
                day = "09" + d[0:2] + d[5:]
                t = file_name[2]
                time_crop = t[0:2]
                file_no = file_no + 1
                f = h5py.File(filepath, 'r')
                #print(file_no)
                f.close()
        except IOError as e:
            print(file_name)
            os.remove(filepath)
        except IndexError as i:
            print(file_name)
        except ValueError as v:
            print(file_name)
            os.remove(filepath)
        except Exception as a:
            print(file_name)