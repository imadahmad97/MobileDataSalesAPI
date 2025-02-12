from fastapi import FastAPI, Request
from app.service.mobile_data_purchase_processor import (
    process_mobile_data_purchase_request,
)

app = FastAPI()
# Initialize the database connection


@app.post("/mobile-data-purchase-request")
async def root(request: Request):
    response = await process_mobile_data_purchase_request(request)
    return response
