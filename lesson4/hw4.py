# Выберем в качестве примера страницу, содержащую простую табличную информацию для парсинга.
# Возьмем, например, состав ФК "Зенит" и основные данные о его футболистах с сайта transfermarkt
import datetime

import lxml
import requests
from lxml import html
import csv

# URL для запроса данных
url = 'https://www.transfermarkt.com/zenit-st-petersburg/startseite/verein/964'

# Заголовки запроса, включая строку агента пользователя
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
}

# Вспомогательная функция для преобразования данных о стоимости прав на игрока в число
def get_market_value(txt: str):
    if txt[-1] == "m":
        value = float(txt[1:-1]) * 1_000_000
    elif txt[-1] == "k":
        value = float(txt[1:-1]) * 1_000
    else:
        value = float(txt[1:])
    return int(value)


# Вспомогательная функция для преобразования данных о дате рождения игрока в формат даты
def convert_to_date(txt: str):
    date_time_obj = datetime.datetime.strptime(txt, '%b %d, %Y')
    return date_time_obj.date()


try:
    # Отправление запроса на получение данных с указанными заголовками
    response = requests.get(url, headers=headers)

    # Проверка, что запрос был успешным
    response.raise_for_status()

    # Использование lxml для анализа полученного HTML
    tree = html.fromstring(response.content)

    # Определение XPath для выбора интересующих нас данных таблицы
    # Например, для transfermarkt пути могут быть следующими:

    squad_numbers = tree.xpath('//div[contains(@class,"rn_nummer")]//text()')
    squad_numbers = [int(x) for x in squad_numbers]

    positions = tree.xpath('//table[contains(@class,"inline-table")]//tr[2]/td//text()')
    positions = [x.strip().replace("\n","") for x in positions]


    names = tree.xpath('//table[contains(@class,"inline-table")]//tr[1]/td[contains(@class,"hauptlink")]//text()')
    names = [x.strip() for x in names if len(x.strip())>0]


    birth_info = tree.xpath('//table[contains(@class,"items")]/tbody//td[contains(@class,"zentriert")]//text()')
    birth_info = [x[:-5].strip() for x in birth_info if len(x[:-5].strip())>0]
    birth_info = [convert_to_date(x) for x in birth_info]



    market_value = tree.xpath('//table[contains(@class,"items")]/tbody//td[contains(@class,"rechts hauptlink")]/a//text()')
    market_value = [x.strip() for x in market_value]
    market_value_eur = [get_market_value(x) for x in market_value]




    # Сравнение стран и столиц (предполагается, что каждой стране соответствует столица)
    data = zip(positions, squad_numbers, names, birth_info, market_value_eur)

    # Сохранение данные в CSV
    with open('fczenit.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Position",
                            "Squad number",
                            "Full name",
                            "Date of birth",
                            "Market value (in euros)"])  # Заголовки столбцов
        csvwriter.writerows(data)

# проверки
except requests.HTTPError as e:
    print(f"Ошибка запроса HTTP: {e}")
except requests.RequestException as e:
    print(f"Ошибка запроса: {e}")
except lxml.etree.ParserError as e:
    print(f"Ошибка парсинга HTML: {e}")
except Exception as e:
    print(f"Ошибка: {e}")

