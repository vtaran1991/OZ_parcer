import bs4
import csv
import requests
import re
import time

start = time.time()

def bookInfoScrapper(bookPageLink):
    responce = requests.get(bookPageLink)
    if responce.status_code != 200:
        return
    else:
        soup = bs4.BeautifulSoup(responce.text, 'html.parser')

        title = soup.find('div', {'class': 'b-product-title__heading'}).get_text().strip()

        if soup.find('a', {'class': 'b-product-title__inner-link'}) != None:
            author = soup.find('a', {'class': 'b-product-title__inner-link'}).get_text().strip()
        else:
            author = ''

        if soup.find('span', {'class': 'b-product-control__text b-product-control__text_main'}) != None:
            price = soup.find('span', {
                'class': 'b-product-control__text b-product-control__text_main'}).get_text().strip()
        else:
            price = ''

        if soup.find('div', {'class': 'b-product-control__sub b-product-control__sub_mover'}) != None:
            status = soup.find('div', {
                'class': 'b-product-control__sub b-product-control__sub_mover'}).get_text().strip()
        else:
            status = ''

        if soup.find('div', {'class': 'b-description__container'}).find(id="truncatedBlock") != None:
            annotation = soup.find('div', {'class': 'b-description__container'}).find(
                id="truncatedBlock").get_text().strip()
        else:
            annotation = ''

        original = ''
        categories = ''
        series = ''
        publisher = ''
        year = ''
        pages = ''
        cover = ''
        age = ''
        formats = ''
        paper = ''
        isbn = ''
        weight = ''
        restrictions = ''
        producer = ''
        importer = ''
        delivery = ''

        tables = soup.find_all('table')
        rows = tables[0].find_all('tr')
        for row in range(len(rows)):
            tds = rows[row].find_all('td')
            if tds[0].get_text() == 'Название в оригинале':
                original = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'Все товары':
                categories = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'Серия':
                series = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'Издательство':
                publisher = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'Год издания':
                year = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'Страниц':
                pages = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'Переплет':
                cover = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'Возраст':
                age = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'Формат':
                formats = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'Бумага':
                paper = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'ISBN':
                isbn = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'Вес':
                weight = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'Возрастные ограничения':
                restrictions = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'Изготовитель':
                producer = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'Импортер':
                importer = tds[1].get_text().replace('\xa0', ' ')
            elif tds[0].get_text() == 'Доставка':
                delivery = tds[1].get_text().replace('\xa0', ' ')
            else:
                continue

    imageLink = soup.find('meta', {'property': 'og:image'}).get('content')
    bookInfo = title, author, price, status, annotation, original, categories, series, publisher, year, pages, cover, age, \
               formats, paper, isbn, weight, restrictions, producer, importer, delivery, imageLink
    return bookInfo

counter = 0

csvFileToRead = open('ALLINONE.csv', 'r')
csvFileToWrite = open('NEW_FINAL.csv', 'w')
reader = csv.reader(csvFileToRead, delimiter=',', quotechar='"', encoding='utf-8')
csvEditor = csv.writer(csvFileToWrite, delimiter=',', quotechar='"', encoding='utf-8')
csvEditor.writerow(["title", "author", "price", "status", "annotation", "original", "categories", "series", \
                        "publisher", "year", "pages", "cover", "age", "formats", "paper", "isbn", "weight", \
                        "restrictions", "producer", "importer", "delivery", "imageLink"])
for row in reader:
    if re.findall('http', row[5]) != []:
        csvEditor.writerow(list(bookInfoScrapper(row[5])))
        counter += 1
        print('Books parced: ' + str(counter))
    else:
        continue
csvFileToRead.close()
csvFileToWrite.close()

end = time.time()

print('Execution time: ' + str(round(end - start, 2)) + ' seconds')
print('Books parced: ' + str(counter))
