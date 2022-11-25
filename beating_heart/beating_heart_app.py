import requests
import json

from gpiozero import LED, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import random
import threading
import os

#Setting GPIOs
factory = PiGPIOFactory()

servo = AngularServo(17, min_angle = -90, max_angle = 90, pin_factory=factory)

green1 = LED(25)
green2 = LED(24)
yellow = LED(23)
red = LED(16)

#Heartbeat function
def heartBeat(bpm, condition):
  
  #Regular
  if bpm > 0 and bpm <= 200:
    wait = ((60 / bpm) - 0.25) / 3

  #Irregular
  if condition == "Irregular":

    randomCase = random.choice(("Up", "Down"))
    randomNum = random.randint(0, 30)

    if randomCase == "Up":
      bpmIrreg = bpm + 10 + randomNum
    if randomCase == "Down":
      bpmIrreg = bpm - 10 - randomNum
    
    wait = ((60 / bpmIrreg) - 0.25) / 3
  
  #Heart Beat
  if bpm > 0 and bpm <= 200:
    sleep(0.25)
    
    servo.angle = -90
    
    green1.on()
    green2.on()
    
    sleep(wait)
    
    green1.off()
    green2.off()
    yellow.on()
    
    sleep(wait)
    
    yellow.off()
    red.on()
    
    sleep(wait)
    
    servo.angle = -30
    
    red.off()

dataJson = '{"bpm": "0", "condition": "Regular", "shutdown": "No"}'
dataDict = json.loads(dataJson)

def api_get():
  while True:
    global dataJson
    global dataDict

    dataJson = requests.get("http://192.168.1.51:5000/database").text
    dataDict = json.loads(dataJson)
    sleep(0.5)

def mainCode():
  while True:
    if dataDict["shutdown"] == "Yes":
      os.system("sudo halt")
    heartBeat(int(dataDict["bpm"]), dataDict["condition"])

threading.Thread(target=api_get).start()
threading.Thread(target=mainCode).start()
