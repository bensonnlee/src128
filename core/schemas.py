from typing import Optional

from pydantic import BaseModel


# Login Model(s)
class AuthPayload(BaseModel):
    """API auth payload model"""

    username: str
    password: str


class BarcodePayload(BaseModel):
    """API barcode payload model"""

    username: str
    password: str
    fusion_key: Optional[str] = ""


# Response Model(s)
class APIResponse(BaseModel):
    """API response model"""

    status_code: int
    error: bool
    message: Optional[str] = ""
    data: Optional[dict]
