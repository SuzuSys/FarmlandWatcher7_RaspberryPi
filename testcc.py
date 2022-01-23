from picamera import PiCamera
from gpiozero import MCP3002, SPISoftwareFallback
import Adafruit_DHT
import time, datetime, csv, json, warnings

warnings.simplefilter("ignore", SPISoftwareFallback)
VREF = 3.3

def sensor(datafile):
  sen0193 = MCP3002(channel=0)
  hum = round(sen0193.value * VREF * 100, 2)
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
  with open(datafile,"a") as output:
    writer = csv.writer(output, delimiter=",", lineterminator="\n")
    writer.writerow(data)

def camera(dir):
  camera = PiCamera()
  camera.start_preview()
  time.sleep(3)
  timeA = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=0)))
  timeC = timeA.strftime('%Y-%m-%d-%H')
  camera.capture(dir + "/" + "%s.jpg" % (timeC))
  camera.stop_preview()
  time.sleep(2)
  camera.close()

PARAMSFILE = 'params.json'

if __name__ == '__main__':
  print(f"loading parameters from {PARAMSFILE}")
  with open(PARAMSFILE, 'r') as f:
    params = json.load(f)
  try:
    sensor(datafile=params["datafile"])
    camera(dir=params["picture-folder"])
  except KeyboardInterrupt:
    print('KeyboardInterrupt.')