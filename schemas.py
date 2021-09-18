
from typing import List, Optional, Dict, Any, ForwardRef
from pydantic import BaseModel, Json, ValidationError, Field, validator, root_validator
from datetime import datetime, timezone
from database import cars_collection, makes_collection, models_collection, submodels_collection





class SubmodelsSchema(BaseModel):
    id: str 
    name: str = None
    active: str = None
    model_id: str = None
    created_at: str
    updated_at: str

    class Config:
        schema_extra = {
            "example": {
                "id":"1000",
                "name": "300",
                "active":"t",
                "model_id":"519",
                "created_at":"2018-06-30 11:16:59+02",
                "updated_at":"2019-08-15 02:02:41.012484+02"
            }
        }




class ModelsSchema(BaseModel):
    id: str 
    name: str
    active: str = None
    make_id: str = None
    created_at: str
    updated_at: str

    class Config:
        schema_extra = {
            "example": {
                "id":"100",
                "name": "x6",
                "active":"t",
                "make_id":"bmw",
                "created_at":"2018-06-30 11:16:59+02",
                "updated_at":"2019-08-15 02:02:41.012484+02"
            }
        }

 

class MakesSchema(BaseModel):
    id: str 
    name: str = None
    active: str = None
    created_at: str
    updated_at: str

    class Config:
        schema_extra = {
            "example": {
                "id":"acura",
                "name":"Acura",
                "active":"t",
                "created_at":"2018-06-30 11:16:59+02",
                "updated_at":"2019-08-15 02:02:41.012484+02"
            }
        }




class CarsSchema(BaseModel):
    id: str 
    active: str = None
    year: str = None
    mileage: str = None
    price: str = None
    make_id: str
    make_name: str = None
    model_id: str
    model_name: str = None
    submodel_id: str
    submodel_name: str = None
    fuel_type: str = None
    exterior_color: str = None
    created_at: str
    updated_at: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        validate_assignment = True




class CarsSchemaOut(BaseModel):
    id: str 
    active: str = None
    year: str = None
    mileage: str = None
    price: str = None
    make_id: str
    model_id: str
    submodel_id: str
    fuel_type: str = None
    exterior_color: str = None
    created_at: str
    updated_at: str







class CarsSchemaIn(BaseModel):
    id: str = Field(...)
    active: str = Field(...)
    year: str = Field(...)
    mileage: int = Field(...)
    price: int = Field(...)
    make_id: str = Field(...)
    model_id: str = Field(...)
    submodel_id: str = Field(...)
    fuel_type: str = Field(...)
    exterior_color: str =Field(...)
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        validate_assignment = True



    @root_validator
    def check_general(cls, values):
        active = values.get('active')
        year = values.get("year")
        mileage = values.get("mileage")
        price = values.get("price")
        if not year.isnumeric():
            raise ValueError('year is not numeric')              
        if active != 't' and active != 'f':
            raise ValueError('active is not correct - it must be t or f')
        return values

    @validator('created_at', pre=True, always=True)
    def default_created(cls, v):
        return v or datetime.utcnow()

    @validator('updated_at', pre=True, always=True)
    def default_updated(cls, v, *, values, **kwargs):
        return v or values['created_at']





class QuerySchemaIn(BaseModel):
    price_low: int = Field(...)
    price_high: int = Field(...)
    mileage_low: int = Field(...)
    mileage_high: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        validate_assignment = True

    @root_validator
    def check_general(cls, values):
        price_low = values.get('price_low')
        price_high = values.get("price_high")
        mileage_low = values.get("mileage_low")
        mileage_high = values.get("mileage_high") 
        if price_low > price_high:
            raise ValueError('price ordering incorrect')
        if mileage_low > mileage_high:
            raise ValueError('mileage ordering incorrect')
        return values







