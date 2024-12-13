from app.schemas import quizEntry_schema
from fastapi import HTTPException, status
from app.db.db import supabase
from typing import List


def join_quiz(participant: quizEntry_schema.Participant):
    try:
        # Check if the quiz exists
        user_id = supabase.table("leaderboard").select("id").eq("room_key", participant.room_key).execute()
        if not user_id.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

        # Register participant
        try:
            result = supabase.table("participants").insert({
                "room_key": participant.room_key,
                "user_id": user_id.data[0]["id"],
                "name": participant.name,
                "score": 0
            }).execute()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to register participant: {e}")

        # Fetch quiz questions
        questions = supabase.table("questions").select("question", "answers", "correct_answer", "time").eq("room_key", participant.room_key).execute()
        if not questions.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No questions found for the quiz")

        response = [quizEntry_schema.questionResponse(
            question=question["question"],
            answers=question["answers"]["answers"],
            correct_answer=question["correct_answer"],
            time=question["time"]
        ) for question in questions.data]

        # Return list of questions
        return quizEntry_schema.Question(
                id=result.data[0]["id"],
                room_key=participant.room_key,
                questions=response
                )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to join quiz: {e}")
    
def update_score(answer: quizEntry_schema.UpdateScore):
    try:
        try:
            # Update the participant's score
            response = supabase.table("participants").update({
                "score": answer.score
            }).eq("id", answer.id).execute()

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update score: {e}")


        # Fetch the updated leaderboard
        leaderboard = supabase.table("participants").select("*").eq("room_key", answer.room_key).order("score", desc=True).execute()

        return [quizEntry_schema.LeaderBoard(
            id=participant["id"],
            room_key=participant["room_key"],
            name=participant["name"],
            score=participant["score"]
        ) for participant in leaderboard.data]

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update score: {e}")
    
def create_room(host_id: int):
    try:
        # create a new room
        response = supabase.table("leaderboard").insert({
            "id": host_id
        }).execute()

        return {"message": "Room created successfully", "room_key": response.data[0]["room_key"]}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create room: {e}")
    
def add_questions(questions: List[quizEntry_schema.AddQuestion], user_id: int, time: int):
    try:
        # create a new room
        room_key = create_room(user_id)["room_key"]

        if not room_key:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create room")

        for question in questions:
            answers_json = {"answers": question.answers}
            supabase.table("questions").insert({
                "room_key": room_key,
                "question": question.question,
                "answers": answers_json,
                "correct_answer": question.correct_answer,
                "time": time
            }).execute()

        print("Questions added successfully")
        return quizEntry_schema.RoomKey(room_key=room_key)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to add questions: {e}")

def delete_room(request: quizEntry_schema.DeleteRoomRequest):
    try:
        # Check if the room exists
        room = supabase.table("leaderboard").select("id").eq("room_key", request.room_key).execute()
        if not room.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

        # Check if the user is the host
        if room.data[0]["id"] != request.user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to delete this room")

        # Delete the participants in the room
        response = supabase.table("participants").delete().eq("room_key", request.room_key).execute()
        if response.data == []:
            # Log the error for debugging, but do not raise an exception
            print(f"Warning: No participants found for the room or failed to delete participants. Room key: {request.room_key}")

        # Delete the questions in the room
        response = supabase.table("questions").delete().eq("room_key", request.room_key).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete questions")

        # Delete the room
        response = supabase.table("leaderboard").delete().eq("room_key", request.room_key).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete room")

        return {"message": "Room deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete room: {e}")
