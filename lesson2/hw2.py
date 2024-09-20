from pprint import pprint
import requests
from bs4 import BeautifulSoup
import json

url = 'https://books.toscrape.com/'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"}
page = 1

sessions = requests.session()

books = []

while True:
    response = sessions.get(url + "catalogue/page-" + str(page) + '.html', headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    book_elements = soup.find_all('article', {'class':'product_pod'})
    # если нет book_elements(при переходе на несуществующую после последней страницу), производится выход из цикла while True
    if not book_elements:
        break
    for element in book_elements:
        title = element.h3.a['title']

        price_float = float(element.find('p', {'class':'price_color'}).text[1:])  # обработка валюты
        price_cur = element.find('p', {'class': 'price_color'}).text[0]  # обработка валюты
        price = (price_float, price_cur)


        # Получить ссылку на страницу с описанием товара
        description_link = element.find('h3').a['href']
        description_url = (url+'catalogue/').replace('index.html', '') + description_link


        # Сделать запрос на страницу с описанием товара
        description_response = requests.get(description_url)
        description_soup = BeautifulSoup(description_response.content, 'html.parser')

        # Получить информацию о наличии товара
        stock_text = description_soup.find('p', {'class': 'instock availability'}).text.strip()
        # Можно добавить дополнительные проверки на наличие цифр в stock_text
        in_stock = int(''.join(filter(str.isdigit, stock_text))) if any(char.isdigit() for char in stock_text) else 0


        # Получить описание товара
        description = description_soup.find('article', {'class': 'product_page'}).find_all('p')[3].text

        book = {
            'title': title,
            'price': price,
            'in_stock': in_stock,
            'description': description
        }
        books.append(book)
    print(f'Обработана страница {page}')
    page+=1



# Сохраняем информацию в JSON-файле
with open('books_data.json', 'w', encoding='utf-8') as file:
    json.dump(books, file, ensure_ascii=False, indent=4)