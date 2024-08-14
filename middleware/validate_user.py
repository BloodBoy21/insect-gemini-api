from fastapi import HTTPException, status
import re
from middleware import create_middleware


async def __validate_user(user_id: str, **kwargs):
    if not re.match(r"^[a-zA-Z0-9]{3,10}$", user_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user id",
        )
    return


validate = create_middleware(callback=__validate_user)
