
from fastapi import Depends, FastAPI, Security
from routers import products
from fastapi.security.api_key import APIKeyHeader
from typing import List
from pydantic import BaseModel
from typing import List



app = FastAPI()


app.include_router(products.router)


