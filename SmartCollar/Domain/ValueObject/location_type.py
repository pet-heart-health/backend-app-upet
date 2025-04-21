import json
from typing import Dict
from pydantic import BaseModel
from sqlalchemy import String, TypeDecorator

class LocationType(BaseModel):
    latitude: float
    longitude: float

 