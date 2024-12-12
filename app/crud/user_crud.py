from app.schemas import user_schema
from fastapi import HTTPException, status
from app.db.db import supabase
from typing import List 

def get_users() -> List[user_schema.UserResponse]:
    try:
        users = supabase.table("users").select("*").execute()
        return users.data
    except Exception as e:
        return{"error": f"Failed to retrieve users: {str(e)}"}
    
def create_user(user: user_schema.UserCreate) -> user_schema.UserResponse:
    try:
        new_user = {"name": user.name, "email": user.email, "is_active": user.is_active, "img_url": user.img_url}
        response = supabase.table("users").insert(new_user).execute()
        return response.data[0]
    except Exception as e:
        return{"error": f"Failed to create user: {str(e)}"}
    
def update_user(user: user_schema.UserUpdate) -> user_schema.UserResponse:
    try:
        updated_user = {"name": user.name, "email": user.email, "is_active": user.is_active, "img_url": user.img_url}
        response = supabase.table("users").update(updated_user).eq("id", user.id).execute()
        return response.data[0]
    except Exception as e:
        return{"error": f"Failed to update user: {str(e)}"}
    
def get_user_by_email(email: str) -> user_schema.UserResponse:
    try:
        user = supabase.table("users").select("*").eq("email", email).execute()
        return user.data[0]
    except Exception as e:
        return{"error": f"Failed to retrieve user: {str(e)}"}
    