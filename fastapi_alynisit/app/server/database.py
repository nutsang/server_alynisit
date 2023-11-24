import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://TGR_GROUP3:ZK984B@mongoDB:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.database_alynisit

hardware_collection = database.get_collection("hardware")
matlab_collection = database.get_collection("matlab")

def hardware_helper(data) -> dict:
    return {
        "id": str(data["_id"]),
        "water_level": data["water_level"],
    }

def matlab_helper(data) -> dict:
    return {
        "id": str(data["_id"]),
        "Day": data["Day"],
        "H": data["H"],
        "Q": data["Q"],
    }

# Get Water Level
async def get_database_water_level():
    water_level = []
    async for document_water_level in hardware_collection.find():
        water_level.append(hardware_helper(document_water_level))
    return water_level

# Post Water Level
async def post_database_water_level(water_data: dict) -> dict:
    water_level_result = await hardware_collection.insert_one(water_data)
    new_water_level = await hardware_collection.find_one({"_id": water_level_result.inserted_id})
    return hardware_helper(new_water_level)

# Post Water Data
async def post_database_water_data(water_data: dict) -> dict:
    water_data_result = await matlab_collection.insert_one(water_data)
    new_water = await matlab_collection.find_one({"_id": water_data_result.inserted_id})
    return matlab_helper(new_water)