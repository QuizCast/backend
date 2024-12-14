from typing import List
from fastapi import APIRouter, Request, HTTPException, Depends
from app.schemas import user_schema
from app.core.config import SUPABASE_URL, SUPABASE_KEY
from app.db.db import supabase
from app.crud import user_crud
from app.utils.autherization import get_current_user

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

@router.put("/update_user", response_model=user_schema.UserResponse, dependencies=[Depends(get_current_user)])
async def update_user(user: user_schema.UserUpdate):
    return user_crud.update_user(user)

@router.get("/get_user/{email}", response_model=user_schema.UserResponse, dependencies=[Depends(get_current_user)])
async def get_user_by_email(email: str):
    return user_crud.get_user_by_email(email)

@router.get("/get_quizHistory/{user_id}", response_model=List[user_schema.AvailableQuiz])
async def get_quiz_history(user_id: int):
    return user_crud.get_quiz_history(user_id)