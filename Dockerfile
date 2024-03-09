FROM alpine:3.19.1

RUN apk update && apk add python3 py3-rpigpio py3-fastapi uvicorn

ENTRYPOINT /bin/sh 
