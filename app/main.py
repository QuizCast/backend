from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import users, quizEntry, auth
from app.db.db import supabase
from app.utils.autherization import auth_middleware


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003",
    "http://localhost:8000",
    "https://quizcast-teamvertex.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(auth_middleware)

app.include_router(users.router)
app.include_router(quizEntry.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"Message": "Welcome to Supabase Hackathon!"}