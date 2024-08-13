from pydantic import BaseModel
from typing import List, Optional, Dict, Union


class BaseResponse(BaseModel):
    success: bool = True
    data: Optional[Union[List, Dict, str]] = None


class ErrorResponse(BaseResponse):
    success: bool = False
    error: Union[str, dict] = "An error occurred"
