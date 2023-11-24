from fastapi import APIRouter 
#fastapi_mqtt
from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi_mqtt.config import MQTTConfig

mqtt_config = MQTTConfig(host = "192.168.1.2",
    port= 1883,
    keepalive = 60,
    username="TGR_GROUP3",
    password="ZK984B")

fast_mqtt = FastMQTT(config=mqtt_config)

router = APIRouter()

fast_mqtt.init_app(router)

from server.database import (
    get_database_water_level,
    post_database_water_level,
)
from server.models.water_model import (
    ResponseModel,
)

@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    fast_mqtt.client.subscribe("mqtt/tgr3") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

# @fast_mqtt.on_message()
# async def message(client, topic, payload, qos, properties):
#     print("Received message: ",topic, payload.decode(), qos, properties)

@fast_mqtt.subscribe("mqtt/tgr3")
async def message_to_topic(client, topic, payload, qos, properties):
    water_data_result = await post_database_water_level({"water_level":float(payload.decode())})
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

@router.get("/", response_description="test publish to mqtt")
async def publish_hello():
    fast_mqtt.publish("mqtt/tgr3", 110.89) #publishing mqtt topic
    return {"result": True,"message":"Published" }
