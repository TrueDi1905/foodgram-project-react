FROM python:3.8.5
WORKDIR /code
COPY backend/requirements.txt .
RUN pip3 install -r requirements.txt
COPY backend/venv .
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000