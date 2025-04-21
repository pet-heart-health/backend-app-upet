from datetime import datetime
from pydantic import BaseModel


class NotificationSchemaPost(BaseModel):
    petOwnerId: int
    type: str
    message: str
    datetime: datetime

class NotificationSchemaGet(BaseModel):
    id: int
    petOwnerId: int
    type: str
    message: str
    datetime: datetime