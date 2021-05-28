#!/usr/bin/python3
import os, requests
from requests.auth import HTTPDigestAuth
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO

BUTTON_PIN = os.getenv('BUTTON_PIN')
CAM_URL = os.getenv('CAM_URL')
CAM_USER = os.getenv('CAM_USER')
CAM_PASS = os.getenv('CAM_PASS')
PUSHOVER_USERS = os.getenv('PUSHOVER_USERS')

print('''Starting Doorbell with the following settings:
BUTTON_PIN: {0}
CAM_URL: {1}
CAM_USER: {2}
CAM_PASS: {3}
PUSHOVER_USERS: {4}
'''.format(BUTTON_PIN or '[unset]', CAM_URL or '[unset]', CAM_USER or '[unset]', '[redacted]' if CAM_PASS else '[unset]', PUSHOVER_USERS or '[unset]'))

if CAM_URL is not None:
  print('{0} - Camera is configured. Authentication may be required.'.format(datetime.now()))
  CAM = True
else:
  print('{0} - Camera is not configured. Notifications will NOT include a picture.'.format(datetime.now()))
  CAM = False

if PUSHOVER_USERS is not None:
  PUSHOVER = True
else:
  print('{0} - Pushover is not configured. Notifications will be sent to stdout.'.format(datetime.now()))
  PUSHOVER = False

print('{0} - Setting up GPIO'.format(datetime.now()))
GPIO.setmode(GPIO.BCM)
GPIO.setup(int(BUTTON_PIN), GPIO.IN)

print('{0} - Setting up sessions'.format(datetime.now()))
CAM_SESSION = requests.Session()
PUSHOVER_SESSION = requests.Session()

if CAM_USER is not None and CAM_PASS is not None:
  print('{0} - Authenticating camera session'.format(datetime.now()))
  CAM_SESSION.auth = HTTPDigestAuth(CAM_USER, CAM_PASS)

print('{0} - Startup complete'.format(datetime.now()))

try:
  pids = []
  while True:
    if BUTTON_PIN is not None:
      if GPIO.wait_for_edge(int(BUTTON_PIN), GPIO.RISING, timeout=5000):
        print('{0} - Rising edge detected'.format(datetime.now()))
        sleep(100 / 1000)

        if GPIO.input(int(BUTTON_PIN)) == GPIO.HIGH:
          print('{0} - Button was pressed'.format(datetime.now()))

          if PUSHOVER:
            pid = os.fork()

            if pid == 0:
              try:
                for PUSHOVER_USER in PUSHOVER_USERS.split(','):
                  PUSHOVER_USER = PUSHOVER_USER.split(':')
                  print('{0} - Sending notification to {1}'.format(datetime.now(), PUSHOVER_USER[0]))
                  PUSHOVER_SESSION.post('https://api.pushover.net/1/messages.json', data={'token': PUSHOVER_USER[1], 'user': PUSHOVER_USER[2], 'priority': PUSHOVER_USER[3], 'message': 'Someone is at the door!\nPicture should follow shortly.'}, timeout=5.0)
              except requests.exceptions.RequestException as exception:
                print('{0} - {1}'.format(datetime.now(), exception))
              os._exit(0)
            else:
              pids.append(pid)
          else:
            print('{0} - Someone is at the door!'.format(datetime.now()))

          if CAM and PUSHOVER:
            pid = os.fork()

            if pid == 0:
              try:
                print('{0} - Retrieving picture from camera'.format(datetime.now()))
                response = CAM_SESSION.get(CAM_URL, timeout=5.0)
                attachment = response.content

                for PUSHOVER_USER in PUSHOVER_USERS.split(','):
                  PUSHOVER_USER = PUSHOVER_USER.split(':')
                  print('{0} - Sending picture to {1}'.format(datetime.now(), PUSHOVER_USER[0]))
                  PUSHOVER_SESSION.post('https://api.pushover.net/1/messages.json', data={'token': PUSHOVER_USER[1], 'user': PUSHOVER_USER[2], 'priority': PUSHOVER_USER[3], 'message': 'See who is at the door!'}, files={'attachment': attachment}, timeout=5.0)
              except requests.exceptions.RequestException as exception:
                print('{0} - {1}'.format(datetime.now(), exception))
              os._exit(0)
            else:
              pids.append(pid)
        else:
          print('{0} - Ignoring; this was probably interference'.format(datetime.now()))

      for cpid in pids:
        spid, status = os.waitpid(cpid, os.WNOHANG)
        if spid == cpid:
          pids.remove(cpid)
    else:
      print('{0} - BUTTON_PIN is required.'.format(datetime.now()))
      sleep(60)
finally:
  print('{0} - Cleaning up GPIO'.format(datetime.now()))
  GPIO.cleanup()
