from picamera import PiCamera
import time
import datetime
import subprocess
from gpiozero import MCP3002

import Adafruit_DHT
import csv
import sys

import schedule

csvfile = "temp.csv"
Vref = 3.3
timeC = ''


def sensor():
  sen0193 = MCP3002(channel=0)
  hum = round(sen0193.value * Vref * 100,2)
  print("WaterLevel = ", str(hum))

  humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22,4)
  if humidity is not None and temperature is not None:
    humidity = round(humidity,2)
    temperature = round(temperature,2)
    print ("Temperature = ", temperature, "*C", "humidity = ", humidity, "%")
  else:
    print ('cannot connect to the sensor you stupid!!!')

  timeA = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=0)))
  timeC = timeA.strftime('%Y-%m-%d %H:%M:%S')
  data = [temperature, humidity, hum, timeC]
      
  with open("/home/pi/Desktop/alltest/temp.csv","a") as output:
    writer = csv.writer(output, delimiter=",", lineterminator="\n")
    writer.writerow(data)
    output.close()

def camera():
  camera = PiCamera()
  camera.start_preview()
  time.sleep(3)
  timeA = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=0)))
  timeC = timeA.strftime('%Y-%m-%d %H:%M:%S')
  camera.capture("/home/pi/Desktop/alltest/pictures/test_%s.jpg" % (timeC))
  
  camera.stop_preview()
  time.sleep(2)
  camera.close()

try:
  sensor()
  camera()
except KeyboardInterrupt:
  print('KeyboardInterrupt.')

