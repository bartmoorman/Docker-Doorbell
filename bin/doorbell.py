#!/usr/bin/python
import os, requests
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO

BUTTON_PIN = os.getenv('BUTTON_PIN')
SYNO_URL = os.getenv('SYNO_URL')
SYNO_ACCOUNT = os.getenv('SYNO_ACCOUNT')
SYNO_PASSWD = os.getenv('SYNO_PASSWD')
SYNO_CAMERA_ID = os.getenv('SYNO_CAMERA_ID')
PUSHOVER_USERS = os.getenv('PUSHOVER_USERS')

print '''Starting Doorbell with the following settings:
BUTTON_PIN: {0}
SYNO_URL: {1}
SYNO_ACCOUNT: {2}
SYNO_PASSWD: {3}
SYNO_CAMERA_ID: {4}
PUSHOVER_USERS: {5}
'''.format(BUTTON_PIN or '[unset]', SYNO_URL or '[unset]', SYNO_ACCOUNT or '[unset]', '[set]' if SYNO_PASSWD else '[unset]', SYNO_CAMERA_ID or '[unset]', PUSHOVER_USERS or '[unset]')

if SYNO_URL is not None and SYNO_ACCOUNT is not None and SYNO_PASSWD is not None and SYNO_CAMERA_ID is not None:
  SYNO = True
else:
  print('{0} - Syno is not configured. Notifications will NOT include a snapshot.'.format(datetime.now()))
  SYNO = False

if PUSHOVER_USERS is not None:
  PUSHOVER = True
else:
  print('{0} - Pushover is not configured. Notifications will be sent to stdout.'.format(datetime.now()))
  PUSHOVER = False

print('{0} - Setting up GPIO'.format(datetime.now()))
GPIO.setmode(GPIO.BCM)
GPIO.setup(int(BUTTON_PIN), GPIO.IN)

print('{0} - Setting up request sessions'.format(datetime.now()))
SYNO_SESSION = requests.Session()
PUSHOVER_SESSION = requests.Session()

try:
  print('{0} - Startup complete'.format(datetime.now()))

  while True:
    if BUTTON_PIN is not None:
      if GPIO.wait_for_edge(int(BUTTON_PIN), GPIO.RISING, timeout=5000):
        print('{0} - Rising edge detected'.format(datetime.now()))
        sleep(100 / 1000)

        if GPIO.input(int(BUTTON_PIN)) == GPIO.HIGH:
          print('{0} - Button was pressed'.format(datetime.now()))
          attachment = None

          if SYNO and PUSHOVER:
            try:
              print('{0} - Logging in to Surveillance Station'.format(datetime.now()))
              SYNO_SESSION.post('{0}/webapi/auth.cgi'.format(SYNO_URL), data={'api': 'SYNO.API.Auth', 'method': 'Login', 'version': 6, 'account': SYNO_ACCOUNT, 'passwd': SYNO_PASSWD, 'session': 'SurveillanceStation'}, timeout=2.5)

              print('{0} - Retrieving snapshot from Surveillance Station'.format(datetime.now()))
              response = SYNO_SESSION.post('{0}/webapi/entry.cgi'.format(SYNO_URL), data={'api': 'SYNO.SurveillanceStation.Camera', 'method': 'GetSnapshot', 'version': 9, 'id': int(SYNO_CAMERA_ID)}, timeout=2.5)
              attachment = response.content
            except requests.exceptions.RequestException as exception:
              print('{0} - {1}'.format(datetime.now(), exception))

          if PUSHOVER:
            for PUSHOVER_USER in PUSHOVER_USERS.split(','):
              PUSHOVER_USER = PUSHOVER_USER.split(':')

              try:
                print('{0} - Sending notification to {1}'.format(datetime.now(), PUSHOVER_USER[0]))
                PUSHOVER_SESSION.post('https://api.pushover.net/1/messages.json', data={'token': PUSHOVER_USER[1], 'user': PUSHOVER_USER[2], 'priority': PUSHOVER_USER[3], 'message': 'Someone is at the door!'}, files={'attachment': attachment or ''}, timeout=5.0)
              except requests.exceptions.RequestException as exception:
                print('{0} - {1}'.format(datetime.now(), exception))
          else:
            print('{0} - Someone is at the door!'.format(datetime.now()))
        else:
          print('{0} - Ignoring; this was probably interference'.format(datetime.now()))
    else:
      print('{0} - BUTTON_PIN is required.'.format(datetime.now()))
      sleep(60)
finally:
  print('{0} - Cleaning up GPIO'.format(datetime.now()))
  GPIO.cleanup()
