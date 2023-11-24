from fastapi import FastAPI
from server.routes.water_route import router as WaterAPIRouter
from server.mqtt.sensor_data import router as MQTTAPIRouter

app = FastAPI()

app.include_router(MQTTAPIRouter, tags=["เส้นทางแห่งเครื่องจักร"], prefix="/mqtt-api-router")
app.include_router(WaterAPIRouter, tags=["เส้นทางแห่งน้ำ"], prefix="/water-api-router")

@app.get("/", tags=["ยินดีต้นรับเข้าสู่เซิฟเวอร์ของ Alynisit"])
async def read_root():
    return {"message": "Hello Welcome to Alynisit server!!!"}