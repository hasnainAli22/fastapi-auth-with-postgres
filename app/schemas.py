from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    content: str
    title: str

    class Config:
        orm_mode = True


class CreatePost(PostBase):
    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] 

    class Config:
        orm_mode = True

class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True

class Token (BaseModel):
    access_token:str
    token_type:str 
    
class DataToken (BaseModel):
    id:Optional[str] = None