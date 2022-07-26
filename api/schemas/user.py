from typing import Optional, List
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr

class UserSchema(BaseModel):
    email: EmailStr = Field(unique=True, index=True)
    password: str
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=True)
    
class UserSchemaUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]
    is_admin: Optional[bool]
    
class UserList(UserSchema):
    _id: str
    email: EmailStr
    
    class Config:
        orm_mode = True

class EmailSchema(BaseModel):
    email: List[EmailStr]

class EmailActivate(BaseModel):
    email: EmailStr
    token: str
    
class ChangePassword(BaseModel):
    oldpwd: str
    newpwd: str
            