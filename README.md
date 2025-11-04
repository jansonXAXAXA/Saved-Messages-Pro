<h1 align="center">Избранное Pro / Favorites Pro</h1>

<p align="center">
  <strong>Ваш персональный архив идей. / Your personal archive of ideas.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-green.svg?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-blue.svg?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Telegram-2CA5E0.svg?logo=telegram&logoColor=white" alt="Telegram Bot">
  <img src="https://img.shields.io/badge/Vue.js-4FC08D.svg?logo=vue.js&logoColor=white" alt="Vue.js">
  <img src="https://img.shields.io/badge/Docker-2496ED.svg?logo=docker&logoColor=white" alt="Docker">
</p>

## 💡 Идея / The Idea

**RU:** Ежедневно мы сохраняем десятки ссылок и постов в "Избранное", которое со временем превращается в хаос. "Избранное Pro" решает эту проблему, организуя контент в визуальные "доски" (как в Pinterest) с удобным поиском и доступом.

**EN:** Every day, we save dozens of links and posts to our "Saved Messages," which turns into chaos over time. "Izbranoe Pro" solves this by organizing content into visual "boards" (like Pinterest) with easy search and access.

## ✨ Технологический стек / Tech Stack

| Компонент | Технологии |
|---|---|
| **Бэкенд / Backend** | `FastAPI`, `SQLAlchemy`, `PostgreSQL` |
| **Telegram-бот / Bot** | `aiogram 3.x` |
| **Веб-интерфейс / Web UI** | `HTML`, `CSS`, `Vue.js` |
| **Окружение / Environment** | `Docker` |

---

## 🛠️ Как запустить проект / How to Run the Project

<details>
<summary><strong>🇷🇺 Инструкция на русском (нажмите, чтобы развернуть)</strong></summary>

**Предварительные требования:** **Git**, **Python 3.10+**, **Docker Desktop**.

#### Шаг 1: Получение кода
*   Клонируйте репозиторий на свой компьютер:
    ```bash
    # Замените URL на адрес вашего репозитория
    git clone https://github.com/YourUsername/YourRepoName.git
    cd YourRepoName
    ```

#### Шаг 2: Настройка переменных окружения
*   В корне проекта создайте файл `.env`.
*   Скопируйте в него текст ниже и **обязательно вставьте ваш токен бота**:
    ```env
    DATABASE_URL=postgresql://user:password@localhost/izbranoe_db
    BOT_TOKEN=12345:ABCDEFG...
    ```

#### Шаг 3: Запуск Базы Данных (Терминал 1)
> **Важно:** Этот компонент должен работать в фоне.

1.  Убедитесь, что **Docker Desktop запущен**.
2.  Откройте терминал и выполните команду:
    ```bash
    docker start izbranoe-postgres
    ```
    > *Если вы видите ошибку "No such container", выполните команду для создания контейнера (это нужно сделать только один раз):*
    > ```bash
    > docker run --name izbranoe-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=izbranoe_db -p 5432:5432 -d postgres
    > ```

#### Шаг 4: Запуск Бэкенда (Терминал 2)
> **Важно:** Этот терминал должен оставаться открытым.

1.  Откройте **новый** терминал и перейдите в корень проекта.
2.  Создайте и активируйте виртуальное окружение:
    ```bash
    # Создать venv (если еще не создано)
    python -m venv venv
    # Активировать (Windows)
    .\venv\Scripts\Activate
    ```
3.  Установите все необходимые Python-библиотеки:
    ```bash
    pip install -r requirements.txt
    ```
4.  Запустите сервер FastAPI:
    ```bash
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    *Вы должны увидеть `Uvicorn running on http://0.0.0.0:8000`.*

#### Шаг 5: Запуск Telegram-бота (Терминал 3)
> **Важно:** Этот терминал тоже должен оставаться открытым.

1.  Откройте **еще один новый** терминал и перейдите в корень проекта.
2.  Активируйте то же самое виртуальное окружение:
    ```bash
    .\venv\Scripts\Activate
    ```
3.  Запустите бота:
    ```bash
    python bot.py
    ```
    *Вы должны увидеть `Start polling`.*

#### Шаг 6: Доступ к Веб-интерфейсу
1.  **Терминал не нужен.**
2.  Просто найдите в папке проекта подпапку `frontend`.
3.  Откройте файл `index.html` в вашем браузере.

</details>

<br>

<details>
<summary><strong>🇬🇧 English Instructions (click to expand)</strong></summary>

**Prerequisites:** **Git**, **Python 3.10+**, **Docker Desktop**.

#### Step 1: Clone the Repository
*   Clone the repository to your computer:
    ```bash
    # Replace the URL with your repository's address
    git clone https://github.com/YourUsername/YourRepoName.git
    cd YourRepoName
    ```

#### Step 2: Set Up Environment Variables
*   Create a file named `.env` in the project's root directory.
*   Copy the content below into it and **be sure to insert your bot token**:
    ```env
    DATABASE_URL=postgresql://user:password@localhost/izbranoe_db
    BOT_TOKEN=12345:ABCDEFG...
    ```

#### Step 3: Run the Database (in Terminal 1)
> **Important:** This component must run in the background.

1.  Make sure **Docker Desktop is running**.
2.  Open a terminal and run the command:
    ```bash
    docker start izbranoe-postgres
    ```
    > *If you see a "No such container" error, run the command to create the container instead (this only needs to be done once):*
    > ```bash
    > docker run --name izbranoe-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=izbranoe_db -p 5432:5432 -d postgres
    > ```

#### Step 4: Run the Backend (in Terminal 2)
> **Important:** This terminal must remain open.

1.  Open a **new** terminal and navigate to the project root.
2.  Create and activate a virtual environment:
    ```bash
    # Create venv (if it doesn't exist)
    python -m venv venv
    # Activate (Windows)
    .\venv\Scripts\Activate
    # Activate (macOS/Linux)
    # source venv/bin/activate
    ```
3.  Install all required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
4.  Start the FastAPI server:
    ```bash
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    *You should see `Uvicorn running on http://0.0.0.0:8000`.*

#### Step 5: Run the Telegram Bot (in Terminal 3)
> **Important:** This terminal must also remain open.

1.  Open **another new** terminal and navigate to the project root.
2.  Activate the same virtual environment:
    ```bash
    .\venv\Scripts\Activate
    ```
3.  Start the bot:
    ```bash
    python bot.py
    ```
    *You should see `Start polling`.*

#### Step 6: Access the Web Interface
1.  **No terminal is needed.**
2.  Simply find the `frontend` subfolder in your project directory.
3.  Open the `index.html` file in your favorite web browser.

</details>
