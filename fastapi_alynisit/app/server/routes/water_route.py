import fastapi
import fastapi.encoders

from server.database import (
    get_database_water_level,
    post_database_water_data,
)

from server.models.water_model import (
    WaterSchema,
    ResponseModel,
)

router = fastapi.APIRouter()

@router.get("/", response_description="ดึงข้อมูลระดับน้ำ")
async def get_water_level():
    data = await get_database_water_level()
    if data:
        return ResponseModel(data, 200, "ดึงข้อมูลระดับน้ำสำเร็จ")
    return ResponseModel(data, 404, "ไม่มีข้อมูลระดับน้ำ")

@router.post("/", response_description="เพิ่มข้อมูลน้ำ")
async def post_water_data(water_data: WaterSchema = fastapi.Body(...)):
    convert_water_data = fastapi.encoders.jsonable_encoder(water_data)
    new_water = await post_database_water_data(convert_water_data)
    return ResponseModel(new_water, 200, "เพิ่มข้อมูลน้ำสำเร็จ")