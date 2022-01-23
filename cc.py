from picamera import PiCamera
from gpiozero import MCP3002, SPISoftwareFallback
import Adafruit_DHT
import time, datetime, csv, json, schedule, warnings

warnings.simplefilter("ignore", SPISoftwareFallback)
VREF = 3.3
PARAMSFILE = 'params.json'

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

def timing():
  timing = datetime.datetime.now()
  print(f"now: {timing}")
  minute = 59 - timing.minute
  second = 60 - timing.second
  time.sleep(minute*60 + second)
  timing = datetime.datetime.now()
  print(f"now: {timing}")

if __name__ == '__main__':
  print(f"loading parameters from {PARAMSFILE}")
  with open(PARAMSFILE, 'r') as f:
    params = json.load(f)
  print("Setting the schedule...")
  schedule.every(params["sensor_once_every_hour"]).hours.do(lambda: sensor(datafile=params["datafile"]))
  for t in params["camera_time"]:
    schedule.every().day.at(t).do(lambda: camera(dir=params["picture-folder"]))
  try:
    print("Setting the timing...")
    timing()
    print("Started the sensing.")
    while True:
      schedule.run_pending()
      time.sleep(60*60)
  except KeyboardInterrupt:
    print('KeyboardInterrupt.')