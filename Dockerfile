# Используем базовый образ Alpine с Python 3.12
FROM python:3.12-alpine

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файл с зависимостями Poetry
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Копируем весь проект в контейнер
COPY . .

# Запускаем приложение с помощью Poetry
CMD ["poetry", "run", "python3", "main.py"]