from PIL import Image
import numpy as np
im = Image.open('/home/geospacial2/PycharmProjects/BTP/ndvi_map.tif')
#print(im.mode)
#im.mode = 'I'
#im.show()
print(im.size)

imarray = np.array(im)
print(imarray.shape)
print(imarray)

vegetation = []
for i in range(imarray.shape[0]):
    for j in range(imarray.shape[1]):
        if imarray[i][j] == 255 or imarray[i][j] == 240:
            vegetation.append(-9999)
        else:
            vegetation.append(imarray[i][j])

print(vegetation)