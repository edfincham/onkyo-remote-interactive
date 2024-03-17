FROM python:3.12-alpine

WORKDIR /code

COPY ./main.py /code/
COPY ./onkyo.py /code/

RUN apk add --no-cache build-base && \
    pip install fastapi==0.79.1 uvicorn==0.28.0 RPi.GPIO==0.7.1 && \
    rm -rf ~/.cache/pip && \
    apk del build-base

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
