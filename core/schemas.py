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

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "error": False,
                "message": "Success",
                "data": {
                    "authenticated": True,
                },
            }
        }


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

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "error": False,
                "message": "Success",
                "data": {
                    "barcode_id": "&829379242633&",
                    "fusion_key": "rkSLBJr9fEtq6n1rzSzgzlnJ2HgcSUDSTCHPJJBIjByPGdCUV0OdRt41T2NXFSngNAxQDrTF_8jwPhn7wq5IrQiy1CEFb_77rScsszBQ-DzYCSKlW5b8sjedv4Ow7dgkqW7yN-UoK9Qkq2Knsl6d30ObCbrZB5X53goP7ieErNHMnXM3fCpOS9M70Ud8TNK-F387HwWXNo6-vw1Gb4uXEhffk9tUWohYvWwpzfpbn0E0b2qPO9VYAc9pUjCpul44vVTFxzIeQRaDICdY-iDxV8P5Ry3CW9ytLHrWZKedES0uR7EJ2ho434rOrtL3-cxnQ-ATCGMhsXCmFtYagA4z6FcmzJsh8YlX-4Ir6xNqLdZEdsjpTn8Rw5hz2h74358C",
                },
            }
        }
