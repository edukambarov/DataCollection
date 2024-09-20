from pymongo import MongoClient
import json

client = MongoClient('localhost',27017)

# Создание базы данных
database_name = "hw3_mongodb"
database = client[database_name]

# Создание коллекции и загрузка данных из файла JSON
collection_name = "books_to_scrape"
collection = database[collection_name]

# Чтение данных из файла JSON
with open("books_data.json", encoding='utf-8') as file:
    data = json.load(file)




# Вставка данных в коллекцию
collection.insert_many(data)

# # Поиск книг стоимостью от 30 до 31
for doc in collection.find({'price.0': {'$gt': 30.0, '$lt': 31.0}}):
    print(doc)


# Поиск книг стоимостью от 30 до 31 и с указанием слова "God"
for doc in collection.find({'$and':[{'price.0': {'$gt': 30.0, '$lt': 31.0}},
                                    {'title':{'$regex': 'and', '$options': 'i'}}]
                            }):
    print(doc)

# Закрытие соединения с MongoDB
client.close()
