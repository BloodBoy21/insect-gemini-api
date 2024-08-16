from fastapi import HTTPException, status
import re
from middleware import create_middleware


async def __validate_user(user_id: str, **kwargs):
    if not re.match(
        r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
        user_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user id",
        )
    return


validate = create_middleware(callback=__validate_user)
