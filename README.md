### Docker Run
```
docker run \
--detach \
--name doorbell \
--restart unless-stopped
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
```

### Environment Variables
|Variable|Description|Default|
|--------|-----------|-------|
|TZ|Sets the timezone|`America/Denver`|
|BUTTON_PIN|Sets the input pin to which the button is attached|`17`|
|CAM_URL|Sets the camera's URL for retrieving a picture|`<empty>`|
|CAM_USER|Sets the camera's username|`<empty>`|
|CAM_PASS|Sets the camera's password|`<empty>`|
|PUSHOVER_USERS|Comma-separated list of users (`alias:token:user_or_group_key:priority`) to receive Pushover notifications|`<empty>`|
|PIGPIO_ADDR|Sets the host of pigpiod|`localhost`|
|PIGPIO_PORT|Sets the port of pigpiod|`8888`|
