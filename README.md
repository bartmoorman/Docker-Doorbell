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
|CAM_URL|Sets the camera's URL for retrieving a picture|`<empty>`|
|CAM_USER|Sets the camera's username|`<empty>`|
|CAM_PASS|Sets the camera's password|`<empty>`|
