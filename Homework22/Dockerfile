# Docker-команда FROM вказує базовий образ контейнера
# Наш базовий образ - це Linux з попередньо встановленим python-3.10
FROM python:3.10

# Встановимо змінну середовища
ENV APP_HOME /Homework22

# Встановимо робочу директорію усередині контейнера
WORKDIR $APP_HOME

# Створіть каталоги static і media
RUN mkdir -p /Homework22/hw_project/static
RUN mkdir -p /Homework22/hw_project/media

# Копіюємо файли pyproject.toml і poetry.lock у контейнер
COPY pyproject.toml poetry.lock $APP_HOME/

# Встановимо залежності усередині контейнера
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --only main

# Копіюємо всі інші файли проекту у контейнер
COPY hw_project/ $APP_HOME/hw_project/

# Позначимо порт, на якому працює програма всередині контейнера
EXPOSE 8000

# Запускаємо нашу програму всередині контейнера
CMD ["python", "hw_project/manage.py", "runserver", "0.0.0.0:8000"]

