from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core.schemas import APIResponse


def response_formatter(
    status_code: int,
    message: str = "",
    data: dict = {},
) -> dict:
    """
    Format API responses to be returned in a standardized format

    :param status_code: HTTP status code
    :param message: message to be returned
    :param data: data to be returned

    :returns: dict containing status code, message, and data
    """
    # Determines if the response is an error based on the status code
    is_error = False if status_code < 400 else True
    response = APIResponse(
        status_code=status_code, error=is_error, message=message, data=data
    )

    # Encodes the APIResponse BaseClass as a JSON object
    json_response_data = jsonable_encoder(response)
    response = JSONResponse(status_code=status_code, content=json_response_data)

    return response
