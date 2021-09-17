
from typing import List
from fastapi import APIRouter,  Request,  Security, Depends, HTTPException, status, Body
from motor.metaprogramming import create_class_with_framework
from pydantic import BaseModel
from dependencies import get_user_details
from schemas import CarsSchema, MakesSchema, ModelsSchema, SubmodelsSchema, CarsSchemaIn, CarsSchemaOut
from schemas import QuerySchemaIn
from database import cars_collection, makes_collection, models_collection, submodels_collection
from fastapi_pagination import Page, add_pagination, paginate
from fastapi.encoders import jsonable_encoder
import pymongo


router = APIRouter()



# Retrieve all cars present in the database
@router.get("/cars/",   response_model=Page[CarsSchema], tags=["products"])
async def retrieve_cars(request: Request, token: bool = Depends(get_user_details), ):
    if not request.query_params["page"]  or not request.query_params["page"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Page size or page number is not defined",
        )
    begin = (int(request.query_params["page"])-1) * int(request.query_params["size"])
    size = int(request.query_params["size"])
    if not token:
        return None
    cars_all = []
    async for car in cars_collection.find().skip(begin).limit(size):
        print(car)
        make_name = await makes_collection.find_one({"id": car["make_id"]})
        car["make_name"] = make_name["name"]
        model_name = await models_collection.find_one({"id": car["model_id"]})
        car["model_name"] = model_name["name"]
        submodel_name = await submodels_collection.find_one({"id": car["submodel_id"]})
        if "name" in submodel_name:
            car["submodel_name"] = submodel_name["name"]
        else:
            car["submodel_name"] = None
        cars_all.append(car)
    return paginate(cars_all)



# Retrieve all makes present in the database
@router.get("/makes/", response_model=Page[MakesSchema], tags=["products"])
async def retrieve_makes(token: bool = Depends(get_user_details)):
    print("token result", token )
    if not token:
        return None
    makes_query =  makes_collection.find()
    makes_all = await makes_query.to_list(None)
    return paginate(makes_all)




# Retrieve all models present in the database
@router.get("/models/", response_model=Page[ModelsSchema], tags=["products"])
async def retrieve_models(token: bool = Depends(get_user_details)):
    print("token result", token )
    if not token:
        return None
    models_query =  models_collection.find()
    models_all = await models_query.to_list(None)
    return paginate(models_all)



# Retrieve all submodels present in the database
@router.get("/submodels/", response_model=Page[SubmodelsSchema], tags=["products"])
async def retrieve_submodels(token: bool = Depends(get_user_details)):
    print("token result", token )
    if not token:
        return None
    submodels_query =  submodels_collection.find()
    submodels_all = await submodels_query.to_list(None)
    return paginate(submodels_all)




# Create a new car object 
@router.post("/addcar/",  response_model=CarsSchemaOut, tags=["products"])
async def create_car(new_car: CarsSchemaIn = Body(...), token: bool = Depends(get_user_details) ):
    print("token result", token )
    if not token:
        return None
    new_car = jsonable_encoder(new_car)
    print(new_car["make_id"])
    print(new_car["model_id"])
    print(new_car["submodel_id"])
    make_check = await makes_collection.find_one({"id": new_car["make_id"]})
    if not make_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Make id does not match",
        )

    model_check = await models_collection.find_one({"id": new_car["model_id"]})
    if not model_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model id does not match",
        )    

    submodel_check = await submodels_collection.find_one({"id": new_car["submodel_id"]})
    if not submodel_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Submodel id does not match",
        )

    new_car_obj = await cars_collection.insert_one(new_car)
    created_car = await cars_collection.find_one({"_id": new_car_obj.inserted_id})
    return created_car





# Query cars 
@router.post("/querycar/",  response_model=Page[CarsSchemaOut], tags=["products"])
async def query_car(request: Request, query_car: QuerySchemaIn = Body(...), token: bool = Depends(get_user_details)):
    print(request.query_params["page"])
    print(request.query_params["size"])
    if not request.query_params["page"]  or not request.query_params["page"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Page size or page number is not defined",
        )
    begin = (int(request.query_params["page"])-1) * int(request.query_params["size"])
    size = int(request.query_params["size"])
    if not token:
        return None
    query_car = jsonable_encoder(query_car)
    a = query_car["price_low"]
    b = query_car["price_high"]
    c = query_car["mileage_low"]
    d = query_car["mileage_high"]

    cars_query =  cars_collection.find( {'$and': [{ "mileage": { '$gt' : c, '$lt' : d  }},
                                        { "price": { '$gt' : a, '$lt' : b }} ] }
                                        ).skip(begin).limit(size).sort('updated_at', -1)

    car_docs = await cars_query.to_list(None)
    num=0
    for car in car_docs:
        print(car)
        print(num)
        num = num + 1
    return paginate(car_docs)



add_pagination(router)



