from fastapi import FastAPI
import uuid
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import users


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)

@app.get("/")
def read_root():
    return {"Message": "Welcome to Supabase Hackathon!"}