# FarmlandWatcher7_RaspberryPi

## Requirement for cc.py 
+ gpiozero (pip)
+ Adafruit_DHT (pip)
+ Schedule (pip)

## Requirement for pubsub.py
```
sudo apt-get install cmake
sudo apt-get install python3-dev
python3 -m pip install awsiotsdk
```
## Lisence
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0.
Reference: https://github.com/aws/aws-iot-device-sdk-python-v2.git

## NOTE
# Requirement `params.json`
```
{
  "endpoint": "XXX.iot.XXX.amazonaws.com",
  "prefix_topic": "XXX",
  "sensor_topic": "XXX",
  "request_topic": "XXX",
  "sensor_topic": "XXX",
  "root-ca": "XXX.pem",
  "cert": "XXX.pem.crt",
  "key": "XXX.pem.key",
  "datafile": "XXX.csv",
  "connect-confirm-url": "www.google.com",
  "picture-folder": "XXX",
  "dimension": "XXX",
  "sensor_once_every_hour": X,
  "camera_time": ["XX:XX", ...]
}
```
### Start up by Tera Term
```
nohup python -u cc.py > cc.log &
nohub python -u pubsub.py > pubsub.log &
```
### See which processes are running
```
ps aux | grep cc.py
ps aux | grep pubsub.py
```
### kill
```
kill XXXX
```