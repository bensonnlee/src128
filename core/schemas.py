from typing import Dict, Optional

from pydantic import BaseModel, root_validator


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
class AuthData(BaseModel):
    """API auth data model"""

    authenticated: Optional[bool]


class BarcodeData(BaseModel):
    """API barcode data model"""

    barcode_id: Optional[str]
    fusion_key: Optional[str]
    authenticated: Optional[bool]


class AuthAPIResponse(BaseModel):
    """API auth response model"""

    status_code: int
    error: Optional[bool]
    message: Optional[str] = ""
    data: Optional[AuthData] = {}

    # work around (waiting on https://github.com/samuelcolvin/pydantic/pull/2625)
    @root_validator
    def compute_error(cls, values) -> Dict:
        error = False if values.get("status_code") < 400 else True

        values["error"] = error
        return values


class BarcodeAPIResponse(BaseModel):
    """API barcode response model"""

    status_code: int
    error: Optional[bool]
    message: Optional[str] = ""
    data: Optional[BarcodeData] = {}

    # work around (waiting on https://github.com/samuelcolvin/pydantic/pull/2625)
    @root_validator
    def compute_error(cls, values) -> Dict:
        error = False if values.get("status_code") < 400 else True

        values["error"] = error
        return values
