from fastapi import FastAPI, Request, Depends
from app.service.mobile_data_purchase_processor import (
    process_mobile_data_purchase_request,
)
from app.service.db_service import DatabaseService

app = FastAPI()


@app.post("/mobile-data-purchase-request")
async def mobile_data_purchase_request_route(
    binary_purchase_request: Request,
    db_service: DatabaseService = Depends(DatabaseService.get_db_service),
):
    response = await process_mobile_data_purchase_request(
        binary_purchase_request, db_service
    )

    return response


@app.post("/bulk-mobile-data-purchase-request")
async def bulk_mobile_data_purchase_request_route():
    pass
