# Скачивание страницы с книгами под заказ
import requests, bs4, pprint, time, openpyxl, csv, os
# from selenium import webdriver

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
                'class': 'b-product-control__text b-product-control__text_main'}).get_text().strip().replace('\xa0',
                                                                                                             ' ')
        else:
            price = ''

        if soup.find('div', {'class': 'b-product-control__sub b-product-control__sub_mover'}) != None:
            status = soup.find('div', {
                'class': 'b-product-control__sub b-product-control__sub_mover'}).get_text().strip().replace('\xa0', ' ')
        else:
            status = ''

        if soup.find('div', {'class': 'b-description__container'}).find(id="truncatedBlock") != None:
            annotation = soup.find('div', {'class': 'b-description__container'}).find(
                id="truncatedBlock").get_text().strip().replace('\xa0', ' ')
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
        for row in rows:
            tds = row.find_all('td')
            if tds[0].get_text() == 'Название в оригинале':
                original = tds[1].get_text()
            elif tds[0].get_text() == 'Все товары':
                categories = tds[1].get_text()
            elif tds[0].get_text() == 'Серия':
                series = tds[1].get_text()
            elif tds[0].get_text() == 'Издательство':
                publisher = tds[1].get_text()
            elif tds[0].get_text() == 'Год издания':
                year = tds[1].get_text()
            elif tds[0].get_text() == 'Страниц':
                pages = tds[1].get_text()
            elif tds[0].get_text() == 'Переплет':
                cover = tds[1].get_text()
            elif tds[0].get_text() == 'Возраст':
                age = tds[1].get_text()
            elif tds[0].get_text() == 'Формат':
                formats = tds[1].get_text()
            elif tds[0].get_text() == 'Бумага':
                paper = tds[1].get_text()
            elif tds[0].get_text() == 'ISBN':
                isbn = tds[1].get_text()
            elif tds[0].get_text() == 'Вес':
                weight = tds[1].get_text()
            elif tds[0].get_text() == 'Возрастные ограничения':
                restrictions = tds[1].get_text()
            elif tds[0].get_text() == 'Изготовитель':
                producer = tds[1].get_text()
            elif tds[0].get_text() == 'Импортер':
                importer = tds[1].get_text()
            elif tds[0].get_text() == 'Доставка':
                delivery = tds[1].get_text()
            else:
                continue
    imageLink = soup.find('meta', {'property': 'og:image'}).get('content')
    bookInfo = title, author, price, status, annotation, original, categories, series, publisher, year, pages, cover, age, \
               formats, paper, isbn, weight, restrictions, producer, importer, delivery, imageLink
    print('Book \"' + str(title) + '\" parced')
    return bookInfo

def infoScrapper(pageUrl):
    responce = requests.get(pageUrl)
    responce.raise_for_status()
    soup = bs4.BeautifulSoup(responce.text, 'html.parser')
    booksPerPage = soup.find_all('li', {'class': 'viewer-type-card__li'})
    for z in range(len(booksPerPage)):
        if booksPerPage[z].find('a', {'class': 'item-type-card__link'}) == None:
            continue
        else:
            page = 'https://oz.by' + (booksPerPage[z].find('a', {'class': 'item-type-card__link'}).get('href'))
        with open('KIDS.csv', 'a', encoding='utf-8') as csvFile:
            csvEditor = csv.writer(csvFile, delimiter=',', quotechar='"')
            csvEditor.writerow(bookInfoScrapper(page))
    return

# Парсим послледнюю страницу пагинации
responce = requests.get('https://oz.by/books/topic24.html?availability=1;2;3')
responce.raise_for_status()
soup = bs4.BeautifulSoup(responce.text, 'html.parser')
pagination = soup.find('li', {'class': 'g-pagination__list__li pg-link pg-last'}).get('data-value')
with open('KIDS.csv', 'w', encoding='utf-8') as csvFile:
    csvEditor = csv.writer(csvFile, delimiter=',', quotechar='"')
    csvEditor.writerow(["title", "author", "price", "status", "annotation", "original", "categories", "series", \
                        "publisher", "year", "pages", "cover", "age", "formats", "paper", "isbn", "weight", \
                        "restrictions", "producer", "importer", "delivery", "imageLink"])
# Проходимся по всем страницам пагинации и применяем функцию парсинга
for pageNum in range(1, int(pagination)):
    pageUrl = ('https://oz.by/books/topic24.html?availability=1;2;3&page=' + str(pageNum))
    print(pageUrl)
    infoScrapper(pageUrl)

# infoScrapper('https://oz.by/books/topic24.html?bst=1&sort=best_desc')


# TBD Информация из таблицы сравнивается с выгрузкой из CRM Либрерии и сохраняется список книг, которые в Либрерии есть, а на OZ нет

end = time.time()
print('Execution time: ' + str(round(end - start, 2)) + ' seconds')
# print('Books downloaded: ' + str(len(finalBookList)))
print(os.getcwd())
