FROM python:3.13.2-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY diploma-frontend/dist/diploma_frontend-0.6.tar.gz /app

RUN pip install diploma_frontend-0.6.tar.gz

COPY megano/ ./

RUN python manage.py migrate

RUN python manage.py loaddata megano-fixtures.json

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
