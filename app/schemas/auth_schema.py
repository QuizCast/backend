from typing import Optional, List
from pydantic import BaseModel

class Login(BaseModel):
    email: str
    password: str

class SignUp(BaseModel):
    name: str
    email: str
    password: str
    img_url: Optional[str] = "None"
    is_active: Optional[bool] = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    email: str
    user_id: int
    name: str