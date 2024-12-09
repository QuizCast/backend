from typing import List, Union
from fastapi import APIRouter, Request, HTTPException, Depends, WebSocket, WebSocketDisconnect
from app.schemas import quizEntry_schema
from app.core.config import SUPABASE_URL, SUPABASE_KEY
from app.db.db import supabase
from app.crud import quiz_crud
import json
from app.api.endpoints.webSocket_demo import manager

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"],
)

@router.post("/join", response_model=List[quizEntry_schema.Question])
async def add_participant(participant:quizEntry_schema.Participant ):
    return quiz_crud.join_quiz(participant)


@router.put("/updateScore", response_model=List[quizEntry_schema.LeaderBoard])
async def submit_answer(answer: quizEntry_schema.UpdateScore):
    return quiz_crud.update_score(answer)


@router.post("/addQuestions", response_model=quizEntry_schema.RoomKey)
async def add_question(request: quizEntry_schema.AddQuestionsRequest):
    return quiz_crud.add_questions(request.questions, request.user_id)

@router.websocket("/ws/{room_key}")
async def websocket_endpoint(websocket: WebSocket, room_key: int):
    await manager.connect(websocket, room_key)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_key)


@router.post("/broadcast-message/")
async def broadcast_message(room_key: int, message: str):
    await manager.broadcast(f"{room_key}", json.dumps({"type": "announcement", "message": message}))
    return {"message": "Broadcast sent"}

@router.post("/startQuiz")
async def create_quiz(room_key: int, host_id: int):
    response = supabase.table("leaderboard").insert({
        "room_key": room_key,
        "id": host_id
    }).execute()

    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)

    return {"message": "Quiz created successfully", "room_key": room_key}

