from typing import List, Union
from fastapi import APIRouter, HTTPException, Form, Response
from app.schemas import auth_schema, user_schema
from fastapi.responses import JSONResponse
from app.crud import user_crud
from app.db.db import supabase

router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"],
)

@router.post("/signup", response_model=user_schema.UserResponse)
async def signup(cred: auth_schema.SignUp):
    try:
        auth_response = supabase.auth.sign_up({
            'email': cred.email,
            'password': cred.password,
        })
        
        if auth_response.user is None:
            raise HTTPException(status_code=400, detail="Signup failed")
        
        #  Add user to the database and return user

        user = user_crud.create_user(
            user_schema.UserCreate(
                name=cred.name,
                email=cred.email,
                is_active=cred.is_active,
                img_url=cred.img_url
            )
        )

        return user
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login", response_model=auth_schema.LoginResponse)
async def login(cred: auth_schema.Login):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            'email': cred.email,
            'password': cred.password,
        })
        
        if auth_response.user is None:
            raise HTTPException(status_code=400, detail="Login failed")
        
        access_token = auth_response.session.access_token
        json_response = JSONResponse(content={"message": "Login successful"})
        json_response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=True,  
            samesite="Lax" 
        )

        user = user_crud.get_user_by_email(auth_response.user.email)

        response = auth_schema.LoginResponse(
            access_token=access_token,
            token_type="bearer",
            email=user["email"],
            user_id=user["id"],
            name=user["name"],
            img_url=user["img_url"],
        )

        return response
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/logout")
async def logout(response: Response):
    try:
        response.delete_cookie(key="access_token")
        response = JSONResponse(content={"message": "Logout successful"})
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
