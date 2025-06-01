### 📦 `python-fast-api-tests`

Это учебный проект, демонстрирующий написание автотестов для REST API с использованием библиотеки `pytest`, а также реализацию тестируемого API на `FastAPI`.

---

### 🔧 Стек технологий

- Python 3.10+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pytest](https://docs.pytest.org/)
- [Requests](https://requests.readthedocs.io/)
- [FastAPI Pagination](https://github.com/uriyyo/fastapi-pagination)
- Uvicorn (ASGI-сервер)

---

### 📁 Структура проекта

```
.
├── models/
│   ├── AppStatus.py         # Модель для healthcheck
│   ├── test_user.py         # Модель User
│   └── test_users.json      # Пример данных пользователей
├── tests/
│   ├── conftest.py          # Фикстуры и конфигурация
│   ├── test_requests.py     # Основные автотесты API
│   └── test_smoke.py        # Дополнительные проверки
├── main.py                  # FastAPI-сервис (имитация reqres.in)
└── README.md                # Документация проекта
```

---

### 🚀 Как запустить

#### 1. Клонировать репозиторий

```bash
git clone https://github.com/Andreyshabalinn/python-fast-api-tests.git
cd python-fast-api-tests
```

#### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

Если файла `requirements.txt` пока нет, установи вручную:

```bash
pip install fastapi uvicorn requests pytest python-dotenv fastapi-pagination
```

#### 3. Заполнить `.env`

В корне проекта создай файл `.env`:

```
BASE_URL=http://localhost:8000/api/
```

#### 4. Запустить FastAPI-сервер

```bash
uvicorn main:app --reload
```

Сервис будет доступен по адресу: [http://localhost:8000/api](http://localhost:8000/api)

#### 5. Запустить тесты

```bash
pytest
```

---

### ✅ Что покрыто в тестах

- `/users`
  - Получение всех пользователей
  - Проверка количества
  - Проверка пагинации с использованием fastapi-pagination
- `/users/{id}`
  - Получение пользователя по ID
  - Проверка ошибки 404 на несуществующий ID
- `/users` (POST)
  - Создание нового пользователя с использованием модели `User`
- `/healthcheck`
  - Проверка статуса сервиса
  - Использование модели `AppStatus`

---

### 📌 Зачем это нужно

Этот проект демонстрирует:
- как писать end-to-end тесты для REST API,
- как имитировать поведение внешнего API локально,
- как использовать `Pydantic` для валидации ответов,
- как подключать `fastapi-pagination` для постраничного вывода,
- как структурировать автотесты с использованием фикстур и `.env`.

---

Готов к расширению: можно подключать базу данных, мок-сервисы, авторизацию и прочее.
