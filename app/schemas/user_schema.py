from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    img_url: Optional[str] = "None"
    is_active: bool

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    img_url: Optional[str] = "None"
    is_active: bool

class UserCreate(BaseModel):
    name: str
    email: str
    img_url: Optional[str] = "None"
    is_active: Optional[bool] = True

class UserUpdate(BaseModel):
    id: int
    name: str
    email: str
    img_url: Optional[str] = "None"
    is_active: Optional[bool] = True