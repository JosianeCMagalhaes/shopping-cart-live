from operator import index
from optparse import Option
from typing import Optional
from click import password_option
from pydantic import BaseModel, Field

class CustomerSchema(BaseModel):
    email: str = Field(unique=True, index=True)
    password: str
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=True)
    
class CustomerSchemaUpdate(BaseModel):
    email: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]
    is_admin: Optional[bool]
    
class CustomerList(CustomerSchema):
    _id: str
    email: str
    
    class Config:
        orm_mode = True