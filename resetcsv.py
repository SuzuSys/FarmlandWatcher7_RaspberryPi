import json

PARAMSFILE = 'params.json'

if __name__ == '__main__':
  print(f"loading parameters from {PARAMSFILE}")
  with open(PARAMSFILE, 'r') as f:
    params = json.load(f)
  datafile = params["datafile"]
  print(f"resetting {datafile}")
  with open(datafile, 'w') as f:
    f.writelines(['temp,humidity,waterlevel,timestamp\n'])
  print("finished!")