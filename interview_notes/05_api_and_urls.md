# URL и API

## Основные HTML-страницы

### Главная страница

- URL: `/`
- View: `venues.views.index`
- Назначение: форма выбора города.

### Поиск

- URL: `/search/`
- View: `venues.views.search`
- Query params:
  - `city`;
  - `date`;
  - `resource_type`.
- Назначение: список коворкингов с фильтрами.

Пример:

```text
/search/?city=1&date=2026-05-22&resource_type=workplace
```

### Детальная страница коворкинга

- URL: `/<venue_id>/`
- View: `venues.views.venue_detail`
- Назначение: информация о коворкинге и список свободных слотов.

### Корзина

- URL: `/bookings/cart/`
- View: `bookings.views.cart_detail`
- Назначение: выбранные слоты и общая сумма.

### Добавить/убрать слот из корзины

- URL: `/bookings/cart/toggle/<slot_id>/`
- View: `bookings.views.toggle_cart`
- Назначение: переключить наличие слота в корзине.
- Поддерживает AJAX через заголовок `X-Requested-With: XMLHttpRequest`.

### Checkout

- URL: `/bookings/checkout/`
- View: `bookings.views.checkout`
- Auth: требуется.
- Назначение: создать бронирования по слотам из корзины.

### Мои бронирования

- URL: `/bookings/my-bookings/`
- View: `bookings.views.my_bookings`
- Auth: требуется.

### Отмена бронирования

- URL: `/bookings/cancel/<booking_id>/`
- View: `bookings.views.cancel_booking`
- Auth: требуется.

### Регистрация

- URL: `/users/register/`
- View: `users.views.register`

### Вход

- URL: `/users/login/`
- View: `users.views.login_view`

### Выход

- URL: `/users/logout/`
- View: `users.views.logout_view`

## JSON API

Проект использует `JsonResponse`, без Django REST Framework.

## API: список коворкингов

- URL: `/api/venues/`
- Method: `GET`
- Auth: не требуется.

Ответ:

```json
{
  "venues": [
    {
      "id": 1,
      "name": "TechSpace Moscow",
      "city": "Москва",
      "address": "ул. Тверская, д. 1",
      "description": "Описание",
      "image_url": "/media/venues/office.jpg"
    }
  ],
  "count": 1
}
```

## API: детали коворкинга

- URL: `/api/venues/<venue_id>/`
- Method: `GET`
- Auth: не требуется.

Ответ включает данные коворкинга и только доступные слоты:

```json
{
  "id": 1,
  "name": "TechSpace Moscow",
  "city": "Москва",
  "address": "ул. Тверская, д. 1",
  "description": "Описание",
  "image_url": "/media/venues/office.jpg",
  "slots": [
    {
      "id": 101,
      "date": "2026-05-22",
      "start_time": "09:00:00",
      "end_time": "13:00:00",
      "resource_type": "Рабочее место",
      "resource_type_code": "workplace",
      "price": "500.00"
    }
  ],
  "slots_count": 1
}
```

## API: бронирования пользователя

- URL: `/api/bookings/`
- Method: `GET`
- Auth: требуется.

Ответ:

```json
{
  "bookings": [
    {
      "id": 55,
      "venue_name": "TechSpace Moscow",
      "date": "2026-05-22",
      "start_time": "09:00:00",
      "end_time": "13:00:00",
      "status": "Подтверждена",
      "status_code": "confirmed",
      "price": "500.00"
    }
  ],
  "count": 1
}
```

## Почему без DRF

Для простого проекта достаточно `JsonResponse`, потому что API небольшое:

- нет сложной сериализации;
- нет версионирования;
- нет токенов;
- нет вложенной бизнес-логики;
- нет необходимости в ViewSet/Serializer.

На собеседовании можно сказать:

«Я понимаю, что для большого API лучше использовать DRF, но в этом проекте API небольшое, поэтому я сделал его средствами Django через `JsonResponse`. Это проще и не добавляет лишнюю зависимость.»

## Что можно улучшить в API

- добавить DRF;
- добавить сериализаторы;
- добавить авторизацию по токенам/JWT;
- добавить OpenAPI/Swagger;
- добавить фильтрацию API по городу, дате и типу ресурса;
- добавить нормальные HTTP-коды ошибок;
- добавить тесты API.

