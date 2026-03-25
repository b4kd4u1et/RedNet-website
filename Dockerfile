FROM python:3.11-slim

WORKDIR /app

# Зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Исходники
COPY . .

# Статика собирается при сборке образа
RUN DJANGO_SECRET_REDNET=build-placeholder python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "RedNet.wsgi", "--bind", "0.0.0.0:8000", "--workers", "2"]
