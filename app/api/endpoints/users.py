from typing import List
from fastapi import APIRouter, Request, HTTPException, Depends
from app.schemas import user_schema
from app.core.config import SUPABASE_URL, SUPABASE_KEY
from app.db.db import supabase
from app.crud import user_crud

router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@router.post("/users", response_model=List[user_schema.UserResponse])
async def get_users():
    return user_crud.get_users()

@router.post("/create_user", response_model=user_schema.UserResponse)
async def create_user(user: user_schema.UserCreate):
    return user_crud.create_user(user)