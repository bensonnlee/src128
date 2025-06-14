import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
import traceback

import uvicorn
from decouple import config
from fastapi import FastAPI
from logdna import LogDNAHandler

from core.main import authenticate, generate_id
from core.schemas import (
    AuthAPIResponse,
    AuthPayload,
    BarcodeAPIResponse,
    BarcodePayload,
)

app = FastAPI(docs_url="/")

# Set up logging with LogDNA
log = logging.getLogger("logdna")
log.setLevel(logging.INFO)
log_dna = LogDNAHandler(config("LOGDNA_INGESTION_KEY"))
log.addHandler(log_dna)


@app.post(
    "/authenticate",
    response_model=AuthAPIResponse,
    response_model_exclude_none=True,
)
def verify_credentials(
    auth_payload: AuthPayload,
):
    """
    Authenticate user credentials

    :param auth_payload:
    """
    try:
        authenticated = authenticate(auth_payload.username, auth_payload.password)

        if authenticated:
            return dict(
                status_code=200,
                message="Success",
                data={"authenticated": True},
            )
        else:
            return dict(
                status_code=401,
                message="Invalid credentials",
                data={"authenticated": False},
            )
    except Exception as e:
        log.info(traceback.format_exc())
        return dict(
            status_code=500,
            message=str(e),
        )


@app.post(
    "/barcode_id",
    response_model=BarcodeAPIResponse,
    response_model_exclude_none=True,
)
def generate_barcode(
    barcode_payload: BarcodePayload,
):
    """
    Generate barcode id

    :param barcode_payload:
    """
    try:
        fusion_key, barcode_id = generate_id(
            barcode_payload.username,
            barcode_payload.password,
            barcode_payload.fusion_key,
        )
        if not fusion_key and not barcode_id:
            return dict(
                status_code=401,
                message="Invalid credentials",
                data={"authenticated": False},
            )
        return dict(
            status_code=200,
            message="Success",
            data={"barcode_id": barcode_id, "fusion_key": fusion_key},
        )
    except Exception as e:
        log.info(traceback.format_exc())
        return dict(
            status_code=500,
            message=str(e),
        )


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
