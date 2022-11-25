from gpiozero import LED
from gpiozero import AngularServo
from time import sleep
import random
import threading

#Heartbeat function
def heartBeat(bpm, condition):
  
  servo = AngularServo(17, min_angle = -90, max_angle = 90)

  #LEDs
  green1 = LED(25)
  green2 = LED(24)
  yellow = LED(23)
  red = LED(16)
  
  #Regular
  wait = ((60 / bpm) - 0.25) / 3

  #Irregular
  if condition == "Irregular":

    randomCase = random.choice(("Up", "Down"))
    randomNum = random.randrange(0,31)

    if randomCase == "Up":
      bpmIrreg = bpm + 10 + randomNum
    if randomCase == "Down":
      bpmIrreg = bpm - 10 - randomNum
    
    wait = ((60 / bpmIrreg) - 0.25) / 3
  
  #Heart Beat
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

bpm = 60
condition = "Regular"

def getInput():
  while True:
    global bpm
    bpm = int(input("Enter BPM: "))
    
    global condition
    condition = input("Regular/Irregular: ")

threading.Thread(target=getInput).start()
threading.Thread(target=heartBeat).start()
