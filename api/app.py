import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
import traceback

import uvicorn
from core.main import authenticate, generate_id
from core.response_handler import response_formatter
from core.schemas import AuthPayload, BarcodePayload
from decouple import config
from fastapi import FastAPI
from logdna import LogDNAHandler

app = FastAPI(docs_url="/")

log = logging.getLogger("logdna")
log.setLevel(logging.INFO)
log_dna = LogDNAHandler(config("LOGDNA_INGESTION_KEY"))
log.addHandler(log_dna)


@app.post("/authenticate")
def verify_credentials(
    auth_payload: AuthPayload,
):
    try:
        authenticated = authenticate(auth_payload.username, auth_payload.password)

        if authenticated:
            return response_formatter(
                200, message="Success", data={"authenticated": True}
            )
        else:
            return response_formatter(
                401, message="Invalid credentials", data={"authenticated": False}
            )
    except Exception as e:
        log.info(traceback.format_exc())
        return response_formatter(500, message=str(e), data={})


@app.post("/barcode_id")
def generate_barcode(
    barcode_payload: BarcodePayload,
):
    try:
        fusion_key, barcode_id = generate_id(
            barcode_payload.username,
            barcode_payload.password,
            barcode_payload.fusion_key,
        )

        return response_formatter(
            200,
            message="Success",
            data={"barcode_id": barcode_id, "fusion_key": fusion_key},
        )
    except Exception as e:
        log.info(traceback.format_exc())
        return response_formatter(500, message=str(e))


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
