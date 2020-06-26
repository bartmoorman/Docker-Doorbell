## This is designed for a Raspberry Pi

### Docker Run
```
docker run \
--detach \
--name doorbell \
--restart unless-stopped
--privileged \
--tty \
bmoorman/doorbell:armhf-latest
```

### Docker Compose
```
version: "3.7"
services:
  doorbell:
    image: bmoorman/doorbell:armhf-latest
    container_name: doorbell
    restart: unless-stopped
    privileged: true
    tty: true
```

### Environment Variables
|Variable|Description|Default|
|--------|-----------|-------|
|TZ|Sets the timezone|`America/Denver`|
|BUTTON_PIN|Sets the input pin to which the button is attached|`<empty>`|
|PUSHOVER_USERS|Comma-separated list of users (`alias:token:user_or_group_key:priority`) to receive Pushover notifications|`<empty>`|
|SYNO_URL|Sets the URL (e.g. `http://syno.lan:5000`) of Synology on which Surveillance Station is installed|`<empty>`|
|SYNO_ACCOUNT|Sets the Synology username|`<empty>`|
|SYNO_PASSWD|Sets the Synology password|`<empty>`|
|SYNO_CAMERA_ID|Sets which Surveillance Station camera to pull a snapshot from|`<empty>`|
|SYNO_CAMERA_STREAM|Sets which of the camera's streams to pull a snapshot from|`1`|
