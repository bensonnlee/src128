from typing import Optional

from pydantic import BaseModel


# Login Model(s)
class Auth(BaseModel):
    """API payload model"""

    username: str
    password: str


# Response Model(s)
class APIResponse(BaseModel):
    """API response model"""

    status_code: int
    error: bool
    message: Optional[str] = ""
    data: Optional[dict]
