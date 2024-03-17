FROM python:3.12-alpine

WORKDIR /code

COPY ./main.py /code/
COPY ./onkyo.py /code/

# Combine commands and specify --no-cache to minimise image size
RUN apk add --no-cache build-base && \
    pip install fastapi==0.110.0 uvicorn==0.28.0 RPi.GPIO==0.7.1 && \
    rm -rf ~/.cache/pip && \
    apk del build-base

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
