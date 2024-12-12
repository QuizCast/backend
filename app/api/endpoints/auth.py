from typing import List, Union
from fastapi import APIRouter, HTTPException, Form, Response
from fastapi.responses import JSONResponse
from app.db.db import supabase

router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"],
)

@router.post("/signup")
async def signup(email: str = Form(...), password: str = Form(...)):
    try:
        auth_response = supabase.auth.sign_up({
            'email': email,
            'password': password
        })
        
        if auth_response.user is None:
            raise HTTPException(status_code=400, detail="Signup failed")
        
        return auth_response.user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login")
async def login(response: Response, email: str = Form(...), password: str = Form(...)):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
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
        
        return json_response
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
