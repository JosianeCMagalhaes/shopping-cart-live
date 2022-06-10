import peewee
from typing import Any, List

from pydantic import BaseModel
from pydantic.networks import EmailStr
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res

class CustomerBase(BaseModel):
    name: str
    email: str

class Customer(CustomerBase):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

class CustomerCreate(CustomerBase):
    password: str

class EmailSchema(BaseModel):
    email: List[EmailStr]

class Activate(BaseModel):
    email: EmailStr
    tokem: str

class ChangePassword(BaseModel):
    old_pass: str
    new_pass: str
    
