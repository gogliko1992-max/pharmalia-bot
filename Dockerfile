# 1️⃣ Берём официальный образ Python
FROM python:3.11-slim

# 2️⃣ Устанавливаем рабочую директорию
WORKDIR /app

# 3️⃣ Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ Копируем весь код проекта
COPY . .

# 5️⃣ Указываем переменные окружения
ENV PORT=8080

# 6️⃣ Команда запуска приложения
CMD ["python", "pharmalia_bot.py"]
