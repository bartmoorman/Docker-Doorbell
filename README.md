## This is designed for a Raspberry Pi

### Docker Run
```
docker run \
--detach \
--name doorbell \
--privileged \
--env "SYNO_URL=http://**sub.do.main**:5000" \
--env "SYNO_ACCOUNT=doorbell" \
--env "SYNO_PASSWD=scQWntLwuSWKpPsK" \
--env "SYNO_CAMERA_ID=12" \
--env "SYNO_CAMERA_STREAM=1" \
--env "PUSHOVER_USERS=alias:token:user_or_group_key:priority" \
bmoorman/doorbell:armhf-latest
```

### Docker Compose
```
version: "3.7"
services:
  doorbell:
    image: bmoorman/doorbell:armhf-latest
    container_name: doorbell
    environment:
      - SYNO_URL=http://**sub.do.main**:5000
      - SYNO_ACCOUNT=doorbell
      - SYNO_PASSWD=scQWntLwuSWKpPsK
      - SYNO_CAMERA_ID=12
      - SYNO_CAMERA_STREAM=1
      - PUSHOVER_USERS=alias:token:user_or_group_key:priority
    privileged: true
```
