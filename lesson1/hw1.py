import requests
import json

# Ваши учетные данные API
CLIENT_ID = 'D0PMI2EYLYPYC2H3ECD2VNSOXRVO32A2PUQSRR5CVFJJNSJ5'
CLIENT_SECRET = 'QTWULXUQTDZ1TLRIU3QVRESQTMQLK3XXT3JDBBA4CQAZU1YH'

# # Конечная точка API
endpoint = "https://api.foursquare.com/v3/places/search"

# Определение параметров для запроса API
city = input("Введите название города: ")
category = input("Введите наименование категории: ")

params = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "near": city,
    "query": category,
    "fields":"name,location,rating"
}

headers = {
    "Accept": "application/json",
    "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
}


# Отправка запроса API и получение ответа
response = requests.get(endpoint, params=params, headers=headers)


# Отправка запроса API и получение ответа
response = requests.get(endpoint, params=params,headers=headers) #endpoint = url

# Проверка успешности запроса API
if response.status_code == 200:
    print("Успешный запрос API!")
    data = json.loads(response.text)#парсим в json файл ответ
    venues = data["results"]#получаем список мест из ответа
    for venue in venues: #проходимся по каждому месту в списке
        print("Название:", venue["name"])
        try:
            print("Адрес:", venue["location"]["address"])
        except Exception:
            print("Адрес не найден")
        try:
            print("Рейтинг:", venue["rating"])
        except Exception:
            print("Рейтинг отсутствует")
        print("\n")
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)
# Проверка успешности запроса API
if response.status_code == 200:
    print("Успешный запрос. Вот что нашлось по вашему запосу:")
    data = json.loads(response.text)
    venues = data["results"]
    for venue in venues:
        print("Название:", venue["name"])
        print("Адрес:", venue["location"]["address"])
        print("\n")
else:
    print("Запрос неудадся с кодом состояния:", response.status_code)
    print(response.text)

# тренировка записи полученных данных в файл
with open('response_data.json', 'w') as f:
    json.dump(data, f)