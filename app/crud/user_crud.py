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
    