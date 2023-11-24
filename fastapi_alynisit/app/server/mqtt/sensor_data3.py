from fastapi import APIRouter 
from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi_mqtt.config import MQTTConfig
import json

mqtt_config = MQTTConfig(
    host="192.168.1.2",
    port=1883,
    keepalive=60,
    username="TGR_GROUP3",
    password="ZK984B",
)

from server.models.water_model import (
    ResponseModel,
)

fast_mqtt = FastMQTT(config=mqtt_config)

router = APIRouter()

fast_mqtt.init_app(router)

@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    fast_mqtt.client.subscribe("/alynisits") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@fast_mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("EiEI", payload.decode())
    print("Received message: ",topic, payload.decode(), qos, properties)
    return 0

@fast_mqtt.subscribe("alynisits")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Hello", payload.decode())
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribedNut", client, mid, qos, properties)

@router.get("/publish/alynisits/{message}", response_description="Publish ข้อมูลไปยัง MQTT สำเร็จ topic alynisits")
async def alynisits_publish_to_mqtt(message: str):
    fast_mqtt.publish(message_or_topic="alynisits", payload=message)
    return ResponseModel({"topic": "alynisits", "message": message}, 200, "Publish ข้อมูลไปยัง MQTT สำเร็จ topic alynisits")

@router.get("/subscribe/alynisits", response_description="Subscribe ข้อมูลไปยัง MQTT และบันทึกข้อมูลลงฐานข้อมูลสำเร็จ topic alynisits")
async def alynisits_subscribe_and_save():
    fast_mqtt.subscribe(topics="alynisits")
    return ResponseModel({"topic": "alynisits"}, 200, "Subscribe ข้อมูลไปยัง MQTT และบันทึกข้อมูลลงฐานข้อมูลสำเร็จ topic alynisits")
