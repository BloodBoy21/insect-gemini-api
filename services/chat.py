from services.gemini import create_chat
from helpers.chat import get_user_data, add_data_to_cache
from logging import getLogger
import json
logger = getLogger(__name__)


def manage_chat(message: str, user_id: str):
    try:
        history = get_user_data(user_id)
        first_response = history.pop()
        history = history[::-1]
        history.insert(0, {
            "role": "user",
            "parts": f"you're an model that can analyze insects,please answer any question from this insect:{first_response["parts"]["name"]},You have previously analyzed this insect from an image and identified it for me. Now, as an expert on insects, please answer all my questions about it."
        })
        history.insert(1, {
            "role": "model",
            "parts": f"Sure i have analyzed the insect and i can answer any question about it,i will use the information i have to answer your questions. Current data:{json.dumps(first_response['parts'])}"
        })
        response = create_chat(history, message)
        if not response:
            raise Exception("Chat failed")
        add_data_to_cache(user_id, {"role": "user", "parts": message})
        add_data_to_cache(user_id, {"role": "model", "parts": response})
        return response
    except Exception as e:
        logger.error(str(e))
        return ''
