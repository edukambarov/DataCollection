import json
from pprint import pprint

import lxml
import requests
import wait as wait
from lxml import html
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



# URL для запроса данных

# url = 'https://www.calc.ru/tablitsa-detskikh-razmerov-obuvi.html'
# url =  'https://www.calc.ru/tablitsa-razmerov-odezhdy-devochek.html'
# url = 'https://www.calc.ru/kalkulyator-razmerov-odezhdy.html'

# Заголовки запроса, включая строку агента пользователя
# headers = {
#     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
# }
user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0")

edge_options = Options()
edge_options.add_argument(f'user_agent={user_agent}')
edge_options.add_argument("--disable-popup-blocking");


# Инициализация веб-драйвера
driver = webdriver.Edge(options=edge_options)

# Вспомогательная функция для преобразования данных о стоимости прав на игрока в число
def clean_columns(lst: list[str]):
    for i in range(len(lst)):
        if lst[i].startswith(' '):
            lst[i-1] = lst[i-1] + lst[i]
    return lst




scrapped_data = []

try:
    # Открытие сайта
    driver.get("https://www.calc.ru/kalkulyator-razmerov-odezhdy.html")

    time.sleep(2)
    raw_links = driver.find_elements(By.XPATH, '//a[contains(@class, "n12")][contains(@title,"Таблица")]')
    links = [ele.get_attribute('href') for ele in raw_links]
    time.sleep(2)
    for link in links:
        driver.get(link)
        item = {'url': link}
        wait = WebDriverWait(driver, 20)
        info = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//body')))
        driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
        raw_table_name = driver.find_element(By.XPATH, '//h1[contains(@itemprop, "name")]')
        item['name'] = raw_table_name.text[:-1]
        time.sleep(3)
        cols = driver.find_elements(By.XPATH,'//table[contains(@class,"razmery")]//tr[1]/td/span')
        cols = [ele.text for ele in cols]
        cols = [x for x in clean_columns(cols) if not x.startswith(' ')]

        time.sleep(3)
        table_data = {}
        for i in range(len(cols)):
             sizes = driver.find_elements(By.XPATH,
                f'//table[contains(@class,"razmery")]//tr/td[{i}+1]')
             sizes = [x.text for x in sizes]
             table_data[cols[i]] = sizes[1:]
        item['data'] = table_data
        time.sleep(3)
        scrapped_data.append(item)
        pprint(item)
        print()




except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    # Закрытие браузера
    driver.quit()
    with open('output.json', 'w', encoding='utf-8') as file:
        json.dump(scrapped_data, file, indent=4, ensure_ascii=False)




# for link in table_links:
#     driver.get(link)
#     wait = WebDriverWait(driver, 20)
#     info = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td')))
#     raw_table_name = driver.find_element(By.XPATH, '//h1[contains(@itemprop, "name")]')
#     print(raw_table_name.text)








    # try:
    #     # Wait for the close button to be clickable (you can adjust the timeout as needed)
    #     close_button = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'b - share - popup__form__close')))
    #
    #     # Click the close button
    #     close_button.click()
    #
    #     # Alternatively, you can use JavaScript to click the close button if the regular click doesn't work
    #     # driver.execute_script("arguments[0].click();", close_button)
    #
    #     print("Close button clicked successfully!")
    # except Exception as e:
    #     print("Error while clicking the close button:", str(e))
    # finally:
    #     driver.quit()

    # all_iframes = driver.find_elements(By.TAG_NAME, "iframe")
    # if len(all_iframes) > 0:
    #     print("Ad Found\n")
    #     driver.execute_script("""
    #         var elems = document.getElementsByTagName("iframe");
    #         for(var i = 0, max = elems.length; i < max; i++)
    #              {
    #                  elems[i].hidden=true;
    #              }
    #                           """)
    #     print('Total Ads: ' + str(len(all_iframes)))
    # else:
    #     print('No frames found')

    # wait = WebDriverWait(driver, 150)
    # info = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td')))
    #
    #
    #
    # driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
    # time.sleep(2)
    #
    #
    #
    #
    # raw_table_name = driver.find_element(By.XPATH, '//h1[contains(@itemprop, "name")]')
    # print(raw_table_name.text)








        # wait = WebDriverWait(driver, 30)
        # info = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//footer')))
        # driver.execute_script('window.scrollBy(0,2000)')
        # time.sleep(pause_time)
        #
        # raw_table_name = driver.find_element(By.XPATH,'//h1[contains(@itemprop, "name")]')
        # print(raw_table_name.text)










# def clean_columns(lst: list[str]):
#     for i in range(len(lst)):
#         if lst[i].startswith(' '):
#             lst[i-1] = lst[i-1] + lst[i]
#     return lst
#
# def clean_table_name(lst: list[str]):
#     return lst[0][:-1]
#
#
#
#
# try:
#     # Отправление запроса на получение данных с указанными заголовками
#     response = requests.get(url, headers=headers)
#     # response.encoding = "windows-1251"
#
#     # Проверка, что запрос был успешным
#     response.raise_for_status()
#
#     # Использование lxml для анализа полученного HTML
#     # tree = html.fromstring(response.content)
#
#     encoding = response.apparent_encoding
#     decoded_content = response.content.decode(encoding)
#     tree = html.fromstring(decoded_content)
#
#     # Определение XPath для выбора интересующих нас данных таблицы
#     # Например, для transfermarkt пути могут быть следующими:
#
#
#
#     links = tree.xpath('//a[contains(@class, "n12")][contains(@title,"Таблица")]/@href')
#
#     print(links)
#
#
#
#
#
#     table_dict = {}
#     table_name = tree.xpath('//h1[contains(@itemprop, "name")]/text()')
#     table_name = clean_table_name(table_name)
#
#     cols = tree.xpath('//table[contains(@class,"razmery")]//tr[1]/td/span/text()')
#     cols = [x for x in clean_columns(cols) if not x.startswith(' ')]
#
#     for i in range(len(cols)):
#         table_dict[cols[i]] = tree.xpath(f'//table[contains(@class,"razmery")]//tr/td[{i}+1]/text()')
#
#
# # проверки
# except requests.HTTPError as e:
#     print(f"Ошибка запроса HTTP: {e}")
# except requests.RequestException as e:
#     print(f"Ошибка запроса: {e}")
# except lxml.etree.ParserError as e:
#     print(f"Ошибка парсинга HTML: {e}")
# except Exception as e:
#     print(f"Ошибка: {e}")

