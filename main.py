from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from app.service.db_service import DatabaseService
from app.service.api_request_handler import (
    handle_single_mobile_data_purchase_request,
    handle_bulk_mobile_upload_purchase_request,
)
import logging

logging.getLogger("fontTools").setLevel(logging.ERROR)
logging.getLogger("fontTools.subset").setLevel(logging.ERROR)
logging.getLogger("fontTools.ttLib.ttFont").setLevel(logging.ERROR)
logging.getLogger("weasyprint").setLevel(logging.ERROR)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s",
)

app: FastAPI = FastAPI()


@app.post("/mobile-data-purchase-request")
async def mobile_data_purchase_request_route(
    binary_purchase_request: Request,
    db_service: DatabaseService = Depends(DatabaseService.get_db_service),
) -> JSONResponse:

    logging.info("Received a mobile data purchase request")

    response: JSONResponse = await handle_single_mobile_data_purchase_request(
        binary_purchase_request, db_service
    )

    logging.info("Successfully completed the mobile data purchase request")

    return response


@app.post("/bulk-mobile-data-purchase-request")
async def bulk_mobile_data_purchase_request_route(
    csv_path: str,
    db_service: DatabaseService = Depends(DatabaseService.get_db_service),
) -> JSONResponse:

    logging.info("Received a bulk mobile data purchase request")

    response: JSONResponse = await handle_bulk_mobile_upload_purchase_request(
        csv_path, db_service
    )

    logging.info("Successfully completed the bulk mobile data purchase request")

    return response
