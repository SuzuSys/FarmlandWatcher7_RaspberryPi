# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
from uuid import uuid4
import json, csv, time, http.client

PARAMSFILE = 'params.json'

# MQTT Callback
def on_connection_interrupted(connection, error, **kwargs):
  print("Connection interrupted. error: {}".format(error))

# MQTT Callback
def on_connection_resumed(connection, return_code, session_present, **kwargs):
  print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

def checkInternetHttplib(url, timeout=3):
  conn = http.client.HTTPConnection(url, timeout=timeout)
  try:
    conn.request("HEAD", "/")
    conn.close()
    return True
  except Exception:
    return False

def data_is_nothing(url):
  with open(url, 'r') as f:
    csvreader = csv.reader(f)
    next(csvreader)
    row = next(csvreader, 0)
    return row == 0

def write_csv(url):
  with open(url, "r") as fr:
    lines = fr.readlines()
    data = lines[1].strip().split(',')
    lines[1:2] = []
    with open(url, 'w') as fw:
      fw.writelines(lines)
  return data

if __name__ == '__main__':
  print(f"loading parameters from {PARAMSFILE}")
  with open(PARAMSFILE, 'r') as f:
    params = json.load(f)
  params['client-id'] = str(uuid4())

  print("setting connection...")
  event_loop_group = io.EventLoopGroup(1)
  host_resolver = io.DefaultHostResolver(event_loop_group)
  client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

  mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=params['endpoint'],
    cert_filepath=params['cert'],
    pri_key_filepath=params['key'],
    client_bootstrap=client_bootstrap,
    ca_filepath=params['root-ca'],
    on_connection_interrupted=on_connection_interrupted,
    on_connection_resumed=on_connection_resumed,
    client_id=params['client-id'],
    clean_session=False,
    keep_alive_secs=6)

  while True:
    try:
      if data_is_nothing(url=params['datafile']):
        print("data is nothing")
        time.sleep(params['sensor_once_every_hour']*3600)
      elif not checkInternetHttplib(url=params['connect-confirm-url']):
        print("wifi is nothing")
        time.sleep(5)
      else:
        print("trying to send data to cloud...")
        print("Connecting to {} with client ID '{}'...".format(
          params['endpoint'], params['client-id']))

        # Connect
        connect_future = mqtt_connection.connect()
        connect_future.result()
        print("Connected!")

        # Publish
        while True:
          if data_is_nothing(url=params['datafile']):
            print("finished sending all data.")
            print("Disconnecting...")
            disconnect_future = mqtt_connection.disconnect()
            disconnect_future.result()
            print("Disconnected!")
            time.sleep(60)
            break
          elif not checkInternetHttplib(url=params['connect-confirm-url']):
            print("wifi is nothing.")
            break
          else:
            print("send data to cloud.")
            dictkey = ["temp", "humidity", "waterlevel", "datetime", "dimension"]
            dictdata = write_csv(url=params['datafile'])
            dictdata[0:3] = map(float, dictdata[0:3])
            dictdata.append(params['dimension'])
            message = dict(zip(dictkey, dictdata))
            sensor_topic = params['prefix_topic'] + '/' + params['sensor_topic']
            print("Publishing message to topic '{}': {}".format(sensor_topic, json.dumps(message)))
            mqtt_connection.publish(
              topic=sensor_topic,
              payload=json.dumps(message),
              qos=mqtt.QoS.AT_LEAST_ONCE)
            time.sleep(1)
        time.sleep(1)
    except KeyboardInterrupt:
      print("KeyboardInterrupt.")
      break
    except Exception as e:
      print(e)
      break
