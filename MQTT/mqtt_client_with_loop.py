import json, requests
import paho.mqtt.client as mqtt
from app import getWeather

# from app import correlate_telemetry_and_weather

#For now only dummy request with hardcoded time and location values
def return_json(): 
    payload = {'Year': '2020', 'Month': '06', 'Day': '22', 'Time': '1600', 'LatMin': '52.25', 'LatMax': '52.00', 'LongMin': '-7.25', 'LongMax': '-7.0'}
    url = 'http://localhost:5000/'
    r = requests.get(url,params=payload)
    response = r.text
    # print(response)
    return json.dumps(response)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    topic = "macdata"
    
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# messages=[b"{'sub': [{'time': '2020-10-21T11:01:34.920704', 'p1': {'volt': 231.264, 'freq': 51.4, 'thdv': 31.491, 'hv3': 38.753, 'hv5': 34.57, 'hv7': 49.401}, 'p2': {'volt': 220.165, 'freq': 48.507, 'thdv': 29.562, 'hv3': 44.364, 'hv5': 12.18, 'hv7': 5.972}, 'p3': {'volt': 235.247, 'freq': 49.855, 'thdv': 8.056, 'hv3': 28.896, 'hv5': 9.35, 'hv7': 10.713}}], 'feeder': [{'id': '1234567890-1', 'data': [{'time': '2020-10-21T11:01:34.920704', 'p1': {'load': 0.407, 'act': 2.225, 'app': 2.444, 'pf': 0.897, 'pfload': 0.336, 'react': 0.904, 'hi3': 0.886, 'hi5': 20.402, 'hi7': 5.925, 'thdi': 11.051}, 'p2': {'load': 0.701, 'act': 2.254, 'app': 2.484, 'pf': 0.856, 'pfload': 0.38, 'react': 1.293, 'hi3': 2.258, 'hi5': 35.376, 'hi7': 7.019, 'thdi': 14.185}, 'p3': {'load': 0.92, 'act': 2.205, 'app': 2.575, 'pf': 0.809, 'pfload': 0.579, 'react': 1.374, 'hi3': 39.744, 'hi5': 31.548, 'hi7': 26.154, 'thdi': 19.714}, 'pN': {'load': 0.437}}]}], 'alarm': {'events': []}, 'packet': '1.0.2', 'id': '1234567890'}"]

messages=[]

def on_message(client, userdata, msg):
    topic = "macdata"
    global messages
    print("\nLength of msgs array :",len(messages))
    if len(messages) < 10:                              # While loop here caused the message to loop itself 10 times so values
        try:                                            # were exactly same for 9 out of 10 messages !!!
            messages.append(str(msg.payload))
        except Exception as e:
            print(e)
    else :
        print('Message limit reached, total of: ', len(messages), '\nInitiating CDS API Connection...')
        weather = return_json()
        jsonWeather = json.dumps(weather)
        result = (messages, jsonWeather)
        # Store result
        print("\nRESULT: ",result)
        # print("\nMESSAGES: ",messages)
        messages=[]
        messages.append(msg.payload)


def run_client():
    try:
        client = mqtt.Client() # algo-runner as a name of a client
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect("servo-msgbroker-local", 1883, 60)
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()
    except Exception as e:
        print(e)

def client_connected():
    try :
        client = mqtt.Client() # algo-runner as a name of a client
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect("servo-msgbroker-local", 1883, 60)
        client.disconnect()
    except Exception as e:
        print(e)

# run_client()