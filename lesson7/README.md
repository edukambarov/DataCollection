**Описание**

Целью было вытянуть таблицы размеров обуви, одежды и соответствующего сайта.

На сайте есть условно главная страница, на которой есть ссылки на страницы с таблицами.

Я хотел на выходе получить список словарей (для записи в json), где:

1. Каждый словарь соответствует таблице. Ключи словаря - таблицы:
   
    ```data```(см. ниже), ```url```(кликабельная ссылка),```name```(название таблицы).
   
2. Данные записаны в словарь ```data``` внутри словаря - таблицы, где ключи - названия столбцов,

   а значение - список значений из таблицы.     


**Подход**

Я предварительно прогнал этот сайт через lxml и поэтому использовал ```BY.XPATH```

для того, чтобы получить искомые элементы:

сначала ссылки на страницы с таблицами, потом данные из таблиц.     


**Трудности**

Их по существу две.

1. Всплывающие модальные окна на страницах, содержащих таблицы. Пример: ***popup_add.bmp*** в корневой папке.

    Так и не понял, как их можно закрыть.  Пробовал блок ```KEYS``` с клавишей ```ESC```,

    пытался нагуглить скрипт на JS. Всё тщетно. Закрывал руками.     


2. Некоторые таблицы почему-то не выгрузились или выгрузилось только название, а дальше пусто.

    Пример: ***non_collected_table.bmp*** в корневой папке.      


**Результаты**

Результат содержится в корневой папке в файле ***hw7_output.json***.


