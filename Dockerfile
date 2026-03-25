FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN DJANGO_SECRET_REDNET=build-placeholder python manage.py collectstatic --noinput

# Запускаем не от root — A02 Security Misconfiguration (OWASP)
RUN adduser --disabled-password --gecos '' --uid 1001 appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["gunicorn", "RedNet.wsgi", "--bind", "0.0.0.0:8000", "--workers", "2"]
