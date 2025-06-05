### 📦 `python-fast-api-tests`

Это учебный проект, демонстрирующий написание автотестов для REST API с использованием библиотеки `pytest`, а также реализацию тестируемого API на `FastAPI`.

---

### 🔧 Стек технологий

* Python 3.10+
* [FastAPI](https://fastapi.tiangolo.com/)
* [Pytest](https://docs.pytest.org/)
* [Requests](https://requests.readthedocs.io/)
* SQLModel
* PostgreSQL
* Docker + Docker Compose
* Uvicorn (ASGI-сервер)

---

### 📁 Структура проекта

```
.
├── app/                    # FastAPI-приложение
│   ├── main.py             # Точка входа
│   ├── database/           # Работа с БД и SQLModel
│   ├── models/             # Pydantic и SQLModel модели
│   └── routers/            # Роутеры: users, healthcheck
├── tests/                  # Автотесты на pytest
│   ├── test_requests.py
│   ├── test_smoke.py
│   └── conftest.py
├── .env                    # Переменные окружения (BASE_URL, DB)
├── docker-compose.yml      # Контейнеризация PostgreSQL
├── requirements.txt        # Зависимости
└── README.md               # Документация проекта
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

#### 3. Запустить Docker Compose

```bash
docker-compose up -d
```

Будет развёрнута база PostgreSQL (если она используется в проекте).

#### 4. Запустить FastAPI-сервер

```bash
uvicorn app.main:app --reload
```

Сервис будет доступен по адресу: [http://localhost:8000/api](http://localhost:8000/api)

#### 5. Запустить тесты

В новом терминале:

```bash
pytest
```

---

### ✅ Что покрыто в тестах

* Получение списка пользователей (`GET /users`)
* Получение пользователя по ID (`GET /users/{id}`)
* Обработка несуществующего пользователя (`GET /users/{invalid_id}`)
* Создание нового пользователя (`POST /users`)
* Обновление пользователя (`PATCH /users/{id}`)
* Удаление пользователя (`DELETE /users/{id}`)
* Проверка "здоровья" API (`GET /healthcheck`)

Каждый тест включает проверку:

* статус-кода ответа
* структуры и содержания JSON
* валидации через модели Pydantic

---

### 📌 Зачем это нужно

Этот проект демонстрирует:

* как писать end-to-end тесты для REST API,
* как использовать SQLModel и FastAPI в связке,
* как изолированно запускать API с базой через Docker,
* как удобно поддерживать покрытие CRUD-операций тестами.
