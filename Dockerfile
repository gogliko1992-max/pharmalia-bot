# 1️⃣ Базовый образ Python
FROM python:3.11-slim

# 2️⃣ Рабочая директория
WORKDIR /app

# 3️⃣ Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ Копируем весь код
COPY . .

# 5️⃣ Указываем порт Cloud Run
ENV PORT=8080

# 6️⃣ Запуск Flask
CMD ["python", "pharmalia_bot.py"]
