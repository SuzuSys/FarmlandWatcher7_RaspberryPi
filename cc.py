import datetime
import subprocess
from gpiozero import MCP3002

import Adafruit_DHT
import csv
import sys

Vref = 3.3
timeC = ''

def sensor():
  sen0193 = MCP3002(channel=0)
  hum = round(sen0193.value * Vref * 100,2)
  print(str(hum))

  humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11,4)
  if humidity is not None and temperature is not None:
    humidity = round(humidity,2)
    temperature = round(temperature,2)
    print ("Temperature = ", temperature, "*C", "humidity = ", humidity, "%")
  else:
    print ('cannot connect to the sensor you stupid!!!')


  timeA = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
  timeC = timeA.strftime('%Y-%m-%d %H:%M:%S %Z')
  data = [temperature, humidity, hum, timeC]

  with open("temp.csv","a") as output:
    writer = csv.writer(output, delimiter=",",lineterminator="\n")
    writer.writerow(data)
  #time.sleep(0.5)

def camera():
  camera = PiCamera()
  camera.start_preview()
  time.sleep(3)

  #timeC = time.strftime("%m")+":"+ time.strftime("%d") + ":" + time.strftime("%T")+ ":" + time.strftime("%Y")
  timeA = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
  timeC = timeA.strftime('%Y-%m-%d %H:%M:%S %Z')
  camera.capture("pictures/test_%s.jpg" % (timeC))

  camera.stop_preview()
  time.sleep(2)
  camera.close()

sensor()
camera()