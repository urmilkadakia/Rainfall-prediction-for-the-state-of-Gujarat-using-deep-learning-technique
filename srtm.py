from PIL import Image
import numpy as np
im = Image.open('/home/geospacial2/PycharmProjects/BTP/srtm_map.tif')
#print(im.mode)
#im.mode = 'I'
#im.show()
print(im.size)

imarray = np.array(im)
print(imarray.shape)
print(imarray)

elevation = []
for i in range(imarray.shape[0]):
    for j in range(imarray.shape[1]):
        elevation.append(imarray[i][j])

print(elevation)