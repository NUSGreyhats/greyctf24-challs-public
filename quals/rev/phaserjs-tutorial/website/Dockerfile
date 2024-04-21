FROM python:3 AS src

RUN mkdir /app
COPY . ./app/
WORKDIR /app

CMD ["python3", "-m", "http.server", "8080"]
