from PIL import ImageOps, Image
import os
import time

start = time.time()

files = os.listdir('/Users/van_taran/PycharmProjects/pyStudy/OZ_KIDS_Images_2/')
for t in range(len(files)):
    img = Image.open("/Users/van_taran/PycharmProjects/pyStudy/OZ_KIDS_Images_2/" + files[t])
    height, width = img.size
    newBorder = (0, 0, 0, round(height * 0.015)) # left, up, right, bottom
    img2 = ImageOps.crop(img, newBorder)
    # img2.show()
    img2.save('/Users/van_taran/PycharmProjects/pyStudy/OZ_KIDS_Images_Libreria/' + files[t])
    print('Book image ' + files[t] + ' saved')

end = time.time()
print('Execution time: ' + str(round(end - start, 2)) + ' seconds')