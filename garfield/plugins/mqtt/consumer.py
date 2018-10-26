import logging

import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def connect_cb(topic):
    def on_connect(client, userdata, flags, rc):
        logging.debug("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(topic)
    return(on_connect)

def on_message(client, userdata, msg):
    logging.info("{topic}: {payload}".format(topic=msg.topic, payload=str(msg.payload)))

def run(args, helpers):
	client = mqtt.Client()
	client.on_connect = connect_cb(args.topic)
	client.on_message = on_message

	client.connect(args.ip, args.port, 60)

	client.loop_forever()
