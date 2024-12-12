from typing import Optional, List
from pydantic import BaseModel

class Participant(BaseModel):
    room_key: int
    name: str

class AnswerSubmission(BaseModel):
    room_key: int
    user_id: int
    score: int

class questionResponse(BaseModel):
    question: str
    answers: list
    correct_answer: str
    time: int

class Question(BaseModel):
    id: int
    room_key: int
    questions: List[questionResponse]

class AddQuestion(BaseModel):
    question: str
    answers: list
    correct_answer: str

class AddQuestionsRequest(BaseModel):
    user_id: int
    time: int
    questions: List[AddQuestion]

class RoomKey(BaseModel):
    room_key: int

class UpdateScore(BaseModel):
    room_key: int
    id: int
    score: int

class LeaderBoard(BaseModel):
    id: int
    room_key: int
    name: str
    score: int
