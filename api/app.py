import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn
from core.main import generate_id
from fastapi import FastAPI

from api.schemas import Auth

app = FastAPI(docs_url="/")


@app.post("/barcode_id")
def generate_barcode(
    auth: Auth,
):
    barcode_id = generate_id(auth.username, auth.password)
    return barcode_id


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
