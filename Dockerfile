FROM bmoorman/alpine:3.8

RUN apk add --no-cache \
    python3 \
    py3-rpigpio \
    py3-requests

COPY bin/ /usr/local/bin/

CMD ["doorbell.py"]
