from typing import List, Union
from fastapi import APIRouter, Depends
from app.schemas import quizEntry_schema
from app.core.config import SUPABASE_URL, SUPABASE_KEY
from app.db.db import supabase
from app.crud import quiz_crud
from app.utils.autherization import get_current_user
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

@router.delete("/deleteRoom", dependencies=[Depends(get_current_user)])
async def delete_room(request: quizEntry_schema.DeleteRoomRequest):
    return quiz_crud.delete_room(request)


