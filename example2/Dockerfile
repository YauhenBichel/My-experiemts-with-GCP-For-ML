FROM python:3.7

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP /app/server.py

CMD gunicorn --bind 0.0.0.0:5050 --timeout=600 wsgi:app -w 4

EXPOSE 5050