# Документация API DeskHub

В данном документе описаны публичные API эндпоинты проекта DeskHub.
Все ответы возвращаются в формате **JSON**.

## Базовый URL
Сервер доступен по адресу: `http://localhost:8000`

---

## 1. Коворкинги (Venues)

### 1.1. Получить список всех коворкингов
Возвращает список всех доступных коворкингов с краткой информацией.

*   **URL:** `/api/venues/`
*   **Метод:** `GET`
*   **Auth:** Не требуется

#### Пример ответа:
```json
{
    "venues": [
        {
            "id": 1,
            "name": "TechSpace Moscow",
            "city": "Москва",
            "address": "ул. Тверская, д. 1",
            "description": "Современный коворкинг в центре...",
            "image_url": "/media/venues/office.jpg"
        },
        {
            "id": 2,
            "name": "Creative Hub",
            "city": "Санкт-Петербург",
            "address": "Невский пр., 25",
            "description": "",
            "image_url": null
        }
    ],
    "count": 2
}
```

### 1.2. Получить детали коворкинга и слоты
Возвращает полную информацию о коворкинге и список доступных (свободных) слотов для бронирования.

*   **URL:** `/api/venues/<id>/`
*   **Метод:** `GET`
*   **Auth:** Не требуется
*   **URL Params:** `id=[integer]`

#### Пример ответа:
```json
{
    "id": 1,
    "name": "TechSpace Moscow",
    "city": "Москва",
    "address": "ул. Тверская, д. 1",
    "description": "Современный коворкинг в центре...",
    "image_url": "/media/venues/office.jpg",
    "slots": [
        {
            "id": 101,
            "date": "2023-11-15",
            "start_time": "09:00:00",
            "end_time": "18:00:00",
            "resource_type": "Рабочее место",
            "resource_type_code": "workplace",
            "price": "1500.00"
        },
        {
            "id": 102,
            "date": "2023-11-15",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "resource_type": "Переговорная",
            "resource_type_code": "meeting_room",
            "price": "3000.00"
        }
    ],
    "slots_count": 2
}
```

---

## 2. Бронирования (Bookings)

### 2.1. Получить список бронирований пользователя
Возвращает историю бронирований текущего авторизованного пользователя.

*   **URL:** `/api/bookings/`
*   **Метод:** `GET`
*   **Auth:** Требуется (Session Cookie)
*   **Примечание:** Если пользователь не авторизован, вернет редирект на страницу входа или 403 (в зависимости от настроек middleware, в текущей реализации `@login_required` редиректит).

#### Пример успешного ответа:
```json
{
    "bookings": [
        {
            "id": 55,
            "venue_name": "TechSpace Moscow",
            "date": "2023-11-15",
            "start_time": "09:00:00",
            "end_time": "18:00:00",
            "status": "Подтверждена",
            "status_code": "confirmed",
            "price": "1500.00"
        },
        {
            "id": 54,
            "venue_name": "Creative Hub",
            "date": "2023-11-10",
            "start_time": "14:00:00",
            "end_time": "16:00:00",
            "status": "Отменена",
            "status_code": "canceled",
            "price": "800.00"
        }
    ],
    "count": 2
}
```

---

## Статусы бронирования (`status_code`)
*   `pending` — Ожидает подтверждения
*   `confirmed` — Подтверждена
*   `rejected` — Отклонена
*   `canceled` — Отменена пользователем
*   `completed` — Завершена

## Типы ресурсов (`resource_type_code`)
*   `workplace` — Рабочее место
*   `meeting_room` — Переговорная комната