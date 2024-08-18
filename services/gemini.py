import google.generativeai as genai
import os
from datetime import datetime
import json
import logging
from fastapi import HTTPException, status
import re

logger = logging.getLogger(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")

model = genai.GenerativeModel(model)


def generate_text(prompt: str):
    return model.generate_text(prompt)


def analyze_image(file_path: str, prompt: str, retry: int = 0) -> str:
    if retry > 3:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze image",
        )
    display_name = f"bug_image_${datetime.now().isoformat()}"
    try:
        img_file = genai.upload_file(file_path, display_name=display_name)
        response = model.generate_content([img_file, prompt])
        response_data = re.sub(r"```json|```", "", response.text).strip()
        logger.info(response_data)
        return json.loads(response_data)
    except Exception as e:
        logger.error(str(e))
        return analyze_image(file_path, prompt, retry + 1)


def create_chat(history: list, message: str, retry: int = 0):
    if retry > 3:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create chat",
        )
    try:
        chat = model.start_chat(history=history)
        print("chat", history)
        response = chat.send_message(message)
        print("response", response)
        logger.info(response.text)
        return response.text
    except Exception as e:
        logger.error(str(e))
        return create_chat(history, message, retry + 1)
