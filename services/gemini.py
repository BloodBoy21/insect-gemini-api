import google.generativeai as genai
import os
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")

model = genai.GenerativeModel(model)


def generate_text(prompt: str):
    return model.generate_text(prompt)


def analyze_image(file_path: str, prompt: str) -> str:
    display_name = f"bug_image_${datetime.now().isoformat()}"
    img_file = genai.upload_file(file_path, display_name=display_name)
    response = model.generate_content([img_file, prompt])
    try:
        logger.info(response.text)
        return json.loads(response.text)
    except Exception as e:
        raise {"error": str(e)}
