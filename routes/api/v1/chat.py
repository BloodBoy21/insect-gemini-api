from fastapi import APIRouter, HTTPException, status
from middleware import validate_user
from models.chat import ChatInput
from models.responses import BaseResponse
from services.chat import manage_chat,get_chat_history

chat_router = APIRouter()


@chat_router.post("/{user_id}", response_model=BaseResponse)
@validate_user.validate
async def send_prompt(input: ChatInput, user_id: str):
    if not input.message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is required",
        )
    response = manage_chat(input.message, user_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get response",
        )
    return {"data": response}


@chat_router.get("/{user_id}", response_model=BaseResponse)
@validate_user.validate
async def get_chat(user_id: str):
    response =  get_chat_history(user_id)
    return {"data": response}