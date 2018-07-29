import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("pluton/test")
    client.subscribe("pluton/topic")

def on_message(client, userdata, msg):

    print(msg.topic+" "+str(msg.payload))

    if msg.payload == "34.5":
        print("Received message #1, do something")

    elif msg.payload == "World":
        print("Received message #2, do something else")
    else:
        print(msg.payload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.105", 1883)


client.loop_forever()
