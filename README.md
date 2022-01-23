# FarmlandWatcher7_RaspberryPi

## Installed for cc.py
+ gpiozero (pip)
+ Adafruit_DHT (pip)
+ Schedule (pip)

## Installation for pubsub.py
```
sudo apt-get update
sudo apt-get install cmake
sudo apt-get install python3-dev
python3 -m pip install awsiotsdk
```
## Lisence
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0.
Reference: https://github.com/aws/aws-iot-device-sdk-python-v2.git

## params.json
```
{
  "endpoint": "XXX.iot.XXX.amazonaws.com",
  "topic": "XXX",
  "root-ca": "XXX.pem",
  "cert": "XXX.pem.crt",
  "key": "XXX.pem.key",
  "datafile": "XXX.csv",
  "connect-confirm-url": "www.google.com",
  "picture-folder": "XXX",
  "dimension": "XXX"
}
```