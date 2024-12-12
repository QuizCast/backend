from typing import List, Union
from fastapi import APIRouter, Request, HTTPException, Depends, WebSocket, WebSocketDisconnect
from app.schemas import quizEntry_schema
from app.core.config import SUPABASE_URL, SUPABASE_KEY
from app.db.db import supabase
from app.crud import quiz_crud
import json


router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"],
)

@router.post("/join", response_model=quizEntry_schema.Question)
async def add_participant(participant:quizEntry_schema.Participant ):
    return quiz_crud.join_quiz(participant)


@router.put("/updateScore", response_model=List[quizEntry_schema.LeaderBoard])
async def submit_answer(answer: quizEntry_schema.UpdateScore):
    return quiz_crud.update_score(answer)


@router.post("/addQuestions", response_model=quizEntry_schema.RoomKey)
async def add_question(request: quizEntry_schema.AddQuestionsRequest):
    return quiz_crud.add_questions(request.questions, request.user_id, request.time)


