# Тестовое задание

### Веб-приложение для учёта складских запасов ресурсов 
(доступно по ссылке: https://academy-a-test-task.herokuapp.com/)

#### Данное приложение предоставляет следующие возможности:

1. Получение списка ресурсов на складе.
2. Добавление новых записей ресурсов.
3. Обновление записей о ресурсах.
4. Удаление записей ресурсов.
5. Получение общей стоимости запасов на складе.

### Модель "Resource":

    Схема:
    {
        id: integer
        title: string 
        amount: number
        unit: string
        price: number
        date: string
    }

###### Просмотр списка постов.

_Метод_ ___GET___ - `/resources`

Выходные данные:

    {
        "resources": [
            {
                "title": "string",
                "id": integer,
                "amount": number,
                "unit": "string",
                "price": number,
                "cost": number,
                "date":"string"
            }
        ],
        "total_count": integer
    }

###### Создание записи о ресурсе.

_Метод_ ___POST___ - `/resources`

Входные данные:

    {
        "title": "string",
        "amount": number,
        "unit": "string",
        "price": number,
        "date": "string"
    }

##### Примечания:

- "amount" и "price" не должны быть меньше 0. 
- "date" в формате ISO (YYYY-MM-DD)

Выходные данные:

    {
        "title": "string",
        "id": integer,
        "amount": number,
        "unit": "string",
        "price": number,
        "cost": number,
        "date":"string"
    }


###### Изменение записи о ресурсе.

_Метод_ ___PUT___ - `/resources`

Входные данные:

    {
        "id": integer,
        "title": "string",
        "amount": number,
        "unit": "string",
        "price": number,
        "date": "string"
    }

##### Примечание:

- "id" - идентификатор записи о ресурсе  

Выходные данные:

    {
        "title": "string",
        "id": integer,
        "amount": number,
        "unit": "string",
        "price": number,
        "cost": number,
        "date":"string"
    }

###### Частичное изменение записи о ресурсе.

_Метод_ ___PATCH___ - `/resources`

Входные данные:

    {
        "id": integer, *обязательно
        "title": "string", *опционально
        "amount": number, *опционально
        "unit": "string", *опционально
        "price": number, *опционально
        "date": "string" *опционально
    }

Выходные данные:

    {
        "title": "string",
        "id": integer,
        "amount": number,
        "unit": "string",
        "price": number,
        "cost": number,
        "date":"string"
    }

###### Удаление записи о ресурсе.

_Метод_ ___DELETE___ - `/resources`

Входные данные:

    {
        "id": integer
    }

###### Получение общей стоимости запасов.

_Метод_ ___GET___ - `/total_cost`

Выходные данные:

    {
        "total_cost": number
    }
