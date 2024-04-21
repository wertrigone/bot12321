# Используем официальный образ Python 3.8 как базовый
FROM python:3.8-slim

# Устанавливаем рабочую директорию для приложения
WORKDIR /app

# Копируем файлы зависимостей в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в рабочую директорию
COPY . .

# Команда для запуска бота
CMD ["python", "chatgpt_bot.py"]
