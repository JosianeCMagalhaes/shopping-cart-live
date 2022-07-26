import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from api.schemas.user import UserSchema
from api.schemas.address import AddressList

class OrderSchema(BaseModel):
    user: UserSchema
    price: Decimal = Field(max_digits=10, decimal_places=2)
    paid: bool = Field(default=False)
    create: datetime.datetime = Field(default=datetime.datetime.now())
    address: AddressList
    authority: Optional[str] = Field(max_length=100)

class OrderSchemaUpdate(BaseModel):
    user: Optional[UserSchema]
    price: Optional[float]
    paid: Optional[bool]
    create: Optional[datetime.datetime]
    address: Optional[AddressList]
    authority: Optional[str]


class OrderList(OrderSchema):
    _id: str
    code: str
    
    class Config:
        orm_mode = True