FROM bmoorman/alpine:3.13

RUN apk add --no-cache \
    python3 \
    py3-requests \
    py3-rpigpio

COPY bin/ /usr/local/bin/

CMD ["doorbell.py"]
