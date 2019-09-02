# Скачивание страницы с книгами под заказ
import requests, bs4, time, csv, os
# from selenium import webdriver

start = time.time()

def infoScrapper(pageUrl):
    responce = requests.get(pageUrl)
    responce.raise_for_status()
    soup = bs4.BeautifulSoup(responce.text, 'html.parser')
    booksPerPage = soup.find_all('li', {'class': 'viewer-type-card__li'})

    bookList = []
    for z in range(len(booksPerPage)):
        title = booksPerPage[z].find('p', {'class': 'item-type-card__title'}).get_text()
        author = booksPerPage[z].find('p', {'class': 'item-type-card__info'}).get_text()
        newPrice = booksPerPage[z].find('span', {'class': 'item-type-card__btn'}).get_text().strip().replace('\xa0', ' ').replace('\n', '/')
        if booksPerPage[z].find('small', {'class': 'item-type-card__cost__discount'}) == None:
            discount = 0
        else:
            discount = booksPerPage[z].find('small', {'class': 'item-type-card__cost__discount'}).get_text()
        # oldPrice = booksPerPage[z].find('strike').get_text()
        # Не могу найти текст по тегу strike
        if booksPerPage[z].find('p', {'class': 'item-type-card__stars'}) != None:
            rating = booksPerPage[z].find('p', {'class': 'item-type-card__stars'}).get('title')
        else:
            rating = 'Нет рейтинга'
        page = 'https://oz.by' + (booksPerPage[z].find('a', {'class': 'item-type-card__link'}).get('href'))
        booksInfo = title, author, newPrice, discount, rating, page
        bookList.append(booksInfo)

        # Вывод статуса при закачке
        print('Book \"' + str(title) + '\" downloaded')
    return bookList

# Парсим послледнюю страницу пагинации
responce = requests.get('https://oz.by/books/?availability=1;2;3')
responce.raise_for_status()
soup = bs4.BeautifulSoup(responce.text, 'html.parser')
pagination = soup.find('li', {'class': 'g-pagination__list__li pg-link pg-last'}).get('data-value')

# Проходимся по всем страницам пагинации и применяем функцию парсинга
finalBookList = []
for pageNum in range(1, int(pagination)):
    pageUrl = ('https://oz.by/books/?availability=1;2;3&page=' + str(pageNum))
    finalBookList.extend(infoScrapper(pageUrl))

# Информация из списка записывается в таблицу

# Сохраняем список книг в файл txt
# txtFile = open('N_A from OZ at ' + str(datetime.datetime.now()) + '.txt', 'w')
# for q in range(len(finalBookList)):
#     txtFile.write(str(finalBookList[q]))
# txtFile.close()


# Сохраняем список книг в файл csv
with open('ALLINONE.csv', 'w') as csvFile:
    csvEditor = csv.writer(csvFile, delimiter=',', quotechar='"')
    csvEditor.writerow(["Title", "Author", "New Price", "Discount", "Rating", "Page URL"])
    for l in range(len(finalBookList)):
        csvEditor.writerow(finalBookList[l])



# TBD Информация из таблицы сравнивается с выгрузкой из CRM Либрерии и сохраняется список книг, которые в Либрерии есть, а на OZ нет
end = time.time()
print(round(end - start, 2))
print('Books downloaded: ' + str(len(finalBookList)))