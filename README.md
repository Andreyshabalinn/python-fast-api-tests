### 📦 `python-fast-api-tests`

Это учебный проект QA Guru, демонстрирующий написание автотестов для REST API с использованием библиотеки `pytest`, а также реализацию тестируемого API на `FastAPI`.

---

### 🔧 Стек технологий

* Python 3.10+
* [FastAPI](https://fastapi.tiangolo.com/)
* [Pytest](https://docs.pytest.org/)
* [Requests](https://requests.readthedocs.io/)
* Uvicorn

---

### 📁 Структура проекта

```
.
├── main.py               # FastAPI-сервис (имитация https://reqres.in)
├── test_requests.py      # Набор автотестов
├── test_user.py          # Данные для создания пользователя
└── README.md             # Документация проекта
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

#### 3. Запустить FastAPI-сервер

```bash
uvicorn main:app --reload
```

Сервис будет доступен по адресу: [http://localhost:8000/api](http://localhost:8000/api)

#### 4. Запустить тесты

В новом терминале (не останавливая сервер):

```bash
pytest test_requests.py
```

---

### ✅ Что покрыто в тестах

* Получение списка пользователей
* Получение пользователя по ID
* Обработка несуществующего пользователя
* Получение ресурса по ID
* Создание нового пользователя (POST)
