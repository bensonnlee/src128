from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core.schemas import APIResponse


def response_formatter(
    status_code: int,
    message: str = "",
    data: dict = {},
) -> dict:
    """
    Formats API responses to be returned by all endpoints

    Returns:
        A dict containing a status code, message, data, and optionally a cookie
    """
    # Determines if the response is an erorr based on the status code
    is_error = False if status_code < 400 else True
    response = APIResponse(
        status_code=status_code, error=is_error, message=message, data=data
    )

    # Encodes the APIResponse BaseClass as a JSON object
    json_response_data = jsonable_encoder(response)
    response = JSONResponse(status_code=status_code, content=json_response_data)

    return response
