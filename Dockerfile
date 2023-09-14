# Образ на основании которого будет запускаться наш контейнер
FROM python:3.11.5-alpine3.18

# Создание рабочей директории внутри контейнера
WORKDIR /app

# Копирование файлов в контейре
COPY . /app

# Установка необходимых библиотек
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Прокидывание переменных окружения внутрь контейнера
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Указание на необходимость открытия порта 8000
EXPOSE 8000