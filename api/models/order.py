from datetime import date, datetime
from optparse import Option
from this import s
from typing import Optional
from pydantic import BaseModel, Field, 
from api.models.customer import CustomerSchema

class OrderSchema(BaseModel):
    customer: CustomerSchema
    price: float = Field(max_digits=10, decimal_places=2)
    paid: bool = Field(default=False)
    create: datetime = Field(default=datetime.datetime.now())
    address: str
    authority: str = Optional[Field(max_length=100)]

class OrderSchemaUpdate(BaseModel):
    customer: Optional[CustomerSchema]
    price: Optional[float]
    paid: Optional[bool]
    create: Optional[datetime]
    address: Optional[str]
    authority: Optional[str]


    