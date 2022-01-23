# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
from uuid import uuid4
import json, time, os, http.client, ast, requests

PARAMSFILE = 'params.json'

# MQTT Callback
def on_connection_interrupted(connection, error, **kwargs):
  print("Connection interrupted. error: {}".format(error))

# MQTT Callback
def on_connection_resumed(connection, return_code, session_present, **kwargs):
  print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

# MQTT Callback
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
  result = ast.literal_eval(payload.decode('utf-8'))
  print("Received message from topic '{}': validation: {}".format(topic, result['validation']))
  if result['validation'] == 0:
    return
  upload_url = result['url']
  with open(PARAMSFILE, 'r') as f:
    params = json.load(f)
  dir = params['picture-folder'] + '/'
  for filename, url in upload_url.items():
    pas = dir + filename
    with open(pas, 'rb') as f:
      img = f.read()
    response = requests.put(url, data=img)
    print(response)
    os.remove(pas)
  print('finished uploading!')  

def checkInternetHttplib(url, timeout=3):
  conn = http.client.HTTPConnection(url, timeout=timeout)
  try:
    conn.request("HEAD", "/")
    conn.close()
    return True
  except Exception:
    return False

def picture_is_nothing(url):
  return os.listdir(url) == []

def pictures_list(url):
  return os.listdir(url)

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
      if picture_is_nothing(url=params['picture-folder']):
        print("data is nothing")
        time.sleep(60*60)
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

        # Topics
        request_topic = params['prefix_topic'] + '/' + params['request_topic']
        subscribe_topic = params['prefix_topic'] + '/' + str(uuid4())

        # Subscribe
        print(f"Subscribing topic '{subscribe_topic}'")
        subscribe_future, packet_id = mqtt_connection.subscribe(
          topic=subscribe_topic,
          qos=mqtt.QoS.AT_LEAST_ONCE,
          callback=on_message_received)
        subscribe_result = subscribe_future.result()
        print("Subscribed with {}".format(str(subscribe_result['qos'])))

        # Publish
        message = {
          "dimension": params['dimension'],
          "topic": subscribe_topic,
          "filenames": pictures_list(url=params['picture-folder'])
        }
        print("Publishing message to topic '{}': {}".format(request_topic, json.dumps(message)))
        mqtt_connection.publish(
          topic=request_topic,
          payload=json.dumps(message),
          qos=mqtt.QoS.AT_LEAST_ONCE)
        time.sleep(3600)
    except KeyboardInterrupt:
      print("KeyboardInterrupt.")
      break
    except Exception as e:
      print(e)
      break
