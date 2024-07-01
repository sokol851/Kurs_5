## Программа для работы с вакансиями с HeadHunter + PostgreSQL!

### Программа получает список вакансий от работодателей с наибольшим количеством вакансий.

### Так же есть возможность произвести поиск вакансий определенных работодателей через запятую.
________
# !Внимание!
## Для работы программы у вас должен быть установлен и настроен PostgreSQL.
## Введите свои данные в документ database.ini, стерев окончание ".sample" из названия.
________

### Данные вакансий получаемые по API:

    1. ID вакансии
    2. Наименование вакансии
    3. Заработная плата от
    4. Заработная плата до
    5. Город
    6. Работодатель
    7. Ссылка на вакансию

### Данные работодателей получаемые по API:

    1. ID работодателя.
    2. Название компании
    3. Количество вакансий у этой компании.
    4. Ссылка на работодателя.

### Программу можно запускать через main.py, где будет предложено меню для работы в консоли.

    1. Обновить БД вакансий по работодателям.
    2. Вывести список вакансий из БД.
    3. Получить список компаний и количество вакансий у каждой.
    4. Получить среднюю оплату по вакансиям в БД.
    5. Список вакансий с оплатой выше средней.
    6. Фильтр вакансий по ключевому слову.
    7. Удалить вакансию из БД по ID.
    8. Очистить базу.
    9. Завершить работу.

# База после завершения работы программы не удаляется, вы можете вернуться к ней позже!