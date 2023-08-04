import machine
from time import sleep
import random
import _thread

from secrets import SSID, PW
import lib.mm_wlan as mm_wlan
from lib.microdot import Microdot
from lib.servo import Servo

#Setting GPIOs

servo = Servo(pin_id=4)

led = machine.Pin("LED", machine.Pin.OUT)

green1 = machine.Pin(3, machine.Pin.OUT)
green2 = machine.Pin(2, machine.Pin.OUT)
yellow = machine.Pin(1, machine.Pin.OUT)
red = machine.Pin(0, machine.Pin.OUT)

#Heartbeat function
def heartbeat(bpm, condition):
  delay = 0
  
  if condition == "Irregular":
    randomCase = random.choice(("Up", "Down"))
    randomNum = random.randint(0, 30)

    if randomCase == "Up":
      bpm = bpm + 10 + randomNum
    elif randomCase == "Down":
      bpm = bpm - 10 - randomNum
    
    delay = ((60 / bpm) - 0.25) / 3
  elif bpm > 0 and bpm <= 200:
    #Regular
    delay = ((60 / bpm) - 0.25) / 3

  
  #Heart Beat
  if bpm > 0 and bpm <= 200:
    sleep(0.25)
    
    servo.write(0)

    green1.on()
    green2.on()
    
    sleep(delay)
    
    green1.off()
    green2.off()
    yellow.on()
    
    sleep(delay)
    
    yellow.off()
    red.on()
    
    sleep(delay)
    
    servo.write(60)
    
    red.off()

data = {"bpm": "0", "condition": "Regular"}

def main():
  global data

  while True:
    heartbeat(int(data["bpm"]), data["condition"])

_thread.start_new_thread(main, ())

mm_wlan.connect_to_network(SSID, PW)
app = Microdot()

@app.route("/heart")
def index(request):
    global data
    return data

@app.post("/heart")
def update(request):
    global data
    data = request.json
    return data

try:
  print("Server running.")
  led.on()
  app.run(port=80)
except:
  print("Something went wrong")
  led.off()
  app.shutdown
  machine.reset()
