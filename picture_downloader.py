import csv
import requests
import bs4
import os
import time

start = time.time()

os.makedirs('OZ_KIDS_Images_2', exist_ok=True)
with open('KIDS.csv', 'r') as csvFileToRead:
    reader = csv.reader(csvFileToRead, delimiter=',', quotechar='"')
    counter = 1
    for row in reader:
        try:
            responce = requests.get(row[21])
            responce.raise_for_status()
        except requests.exceptions.MissingSchema:
            continue
        except requests.exceptions.InvalidURL:
            continue
        except FileNotFoundError:
            continue
        with open(('/Users/van_taran/PycharmProjects/pyStudy/OZ_KIDS_Images_2/' + row[0] + '.jpg'), 'wb') as imageFile:
            for chunk in responce.iter_content(100000):
                imageFile.write(chunk)
            print(str(imageFile) + str(counter) + ' downloaded')
            counter += 1

end = time.time()
print('Execution time: ' + str(round(end - start, 2)) + ' seconds')