from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed
import paho.mqtt.client as mqtt
import json

id = '0eae5b2e-4fb0-42cb-a639-f824ccaae930'
client_name = id + 'nightlight_client'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

light_sensor = GroveLightSensor(0)
led = GroveLed(5)


def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['led_on']:
        led.on()
    else:
        led.off()

#subscribed to the server_command topic
mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command

mqtt_client.loop_start()

print("MQTT connected!")

while True:
    light = light_sensor.light
    telemetry = json.dumps({'light' : light})

    print("Sending telemetry ", telemetry)

    #publish to server using the telemetry topic
    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)
