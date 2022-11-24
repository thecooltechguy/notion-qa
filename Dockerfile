FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# gunicorn -k gevent -b 0.0.0.0:8081 app:app
# ENTRYPOINT [ "/bin/bash" ]
ENTRYPOINT [ "gunicorn", "-k", "gevent", "-b", "0.0.0.0:$PORT",  "app:app"]