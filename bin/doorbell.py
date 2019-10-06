#!/usr/bin/python
import RPi.GPIO as GPIO
import os, requests
from datetime import datetime
from time import sleep

buttonPin = int(os.getenv('BUTTON_PIN'))
pressLength = 100 / 1000

synoURL = os.getenv('SYNO_URL')
synoAccount = os.getenv('SYNO_ACCOUNT')
synoPasswd = os.getenv('SYNO_PASSWD')
synoCameraId = int(os.getenv('SYNO_CAMERA_ID'))
synoCameraStream = int(os.getenv('SYNO_CAMERA_STREAM'))

pushUsers = os.getenv('PUSHOVER_USERS').split(',')

print('{0} - Setting up GPIO'.format(datetime.now()))
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN)

print('{0} - Setting up request sessions'.format(datetime.now()))
synoSession = requests.Session()
pushSession = requests.Session()

try:
  print('{0} - Startup complete'.format(datetime.now()))

  while True:
    if GPIO.wait_for_edge(buttonPin, GPIO.RISING, timeout=5000):
      print('{0} - Rising edge detected'.format(datetime.now()))
      sleep(pressLength)

      if GPIO.input(buttonPin) == GPIO.HIGH:
        print('{0} - Button was pressed'.format(datetime.now()))

        try:
          print('{0} - Logging in to Surveillance Station'.format(datetime.now()))
          synoSession.post('{0}/webapi/auth.cgi'.format(synoURL), data={'api': 'SYNO.API.Auth', 'method': 'Login', 'version': 6, 'account': synoAccount, 'passwd': synoPasswd, 'session': 'SurveillanceStation'}, timeout=2.5)

          print('{0} - Retrieving snapshot from Surveillance Station'.format(datetime.now()))
          request = synoSession.post('{0}/webapi/entry.cgi'.format(synoURL), data={'api': 'SYNO.SurveillanceStation.Camera', 'method': 'GetSnapshot', 'version': '8', 'cameraId': synoCameraId, 'camStm': synoCameraStream}, timeout=2.5)
        except:
          request = None

        for pushUser in pushUsers:
          pushUser = pushUser.split(':')
          print('{0} - Sending notification to {1}'.format(datetime.now(), pushUser[0]))

          if request:
            pushSession.post('https://api.pushover.net/1/messages.json', data={'token': pushUser[1], 'user': pushUser[2], 'priority': pushUser[3], 'message': 'Someone is at the door!'}, files={'attachment': request.content}, timeout=5.0)
          else:
            pushSession.post('https://api.pushover.net/1/messages.json', data={'token': pushUser[1], 'user': pushUser[2], 'priority': pushUser[3], 'message': 'Someone is at the door!\n[Preview unavailable]'}, timeout=5.0)
      else:
        print('{0} - Ignoring; this was probably interference'.format(datetime.now()))
finally:
  print('{0} - Cleaning up GPIO'.format(datetime.now()))
  GPIO.cleanup()
