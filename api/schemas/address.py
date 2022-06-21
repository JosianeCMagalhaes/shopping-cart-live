from typing import Optional, List
from pydantic import BaseModel, Field
from api.schemas.user import UserSchema

class Address(BaseModel):
    street: str
    cep: str
    district: str
    city: str
    state: str
    is_delivery: bool = Field(default=True)

class AddressSchema(BaseModel):
    user: UserSchema
    address: List[Address] = []
     
class AddressSchemaUpdate(BaseModel):
    street: Optional[str]
    cep: Optional[str]
    district: Optional[str]
    city: Optional[str]
    state: Optional[str]
    is_delivery: Optional[bool]

class AddressList(AddressSchema):
    _id: str
    user: UserSchema
    
    class Config:
        orm_mode = True