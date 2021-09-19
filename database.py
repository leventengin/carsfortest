

import os
import motor.motor_asyncio
from bson.objectid import ObjectId




MONGO_DETAILS = "mongodb+srv://levent:JWjvPGzPSDfu9M7@cluster0.crz0j.mongodb.net/test"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.carsfortest

cars_collection = database.get_collection("cars")
makes_collection = database.get_collection("makes")
models_collection = database.get_collection("models")
submodels_collection = database.get_collection("submodels")

