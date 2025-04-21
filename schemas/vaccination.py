from pydantic import BaseModel

class VaccinationSchemaPost(BaseModel):
    name: str

class VaccinationSchemaGet(BaseModel):
    id: int
    name: str
