"""
This module contains the routes for the mobile data sales API.

Dependencies:
    - FastAPI
    - Request
    - JSONResponse
    - DataBaseService
    - handle_single_mobile_data_purchase_request
    - handle_bulk_mobile_upload_purchase_request
    - logging
    
Routes:
    - mobile_data_purchase_request_route
    - bulk_mobile_data_purchase_request_route
"""

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from app.service.db_service import DataBaseService
from app.service.api_request_handler import (
    handle_single_mobile_data_purchase_request,
    handle_bulk_mobile_upload_purchase_request,
)
import logging
from sqlalchemy.orm import Session
from typing import Annotated

logging.getLogger("fontTools").setLevel(logging.ERROR)
logging.getLogger("fontTools.subset").setLevel(logging.ERROR)
logging.getLogger("fontTools.ttLib.ttFont").setLevel(logging.ERROR)
logging.getLogger("weasyprint").setLevel(logging.ERROR)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s",
)
db_service = DataBaseService()
DB_SESSION = Annotated[Session, Depends(db_service.get_db_session)]
app: FastAPI = FastAPI()


@app.post("/mobile-data-purchase-request")
async def mobile_data_purchase_request_route(
    binary_purchase_request: Request,
    DB_SESSION: Annotated[Session, Depends(db_service.get_db_session)],
) -> JSONResponse:
    """
    This route handles a single mobile data purchase request.
    """

    logging.info("Received a mobile data purchase request")

    response: JSONResponse = await handle_single_mobile_data_purchase_request(
        binary_purchase_request, DB_SESSION
    )

    logging.info("Successfully completed the mobile data purchase request")

    return response


@app.post("/bulk-mobile-data-purchase-request")
async def bulk_mobile_data_purchase_request_route(
    csv_path: str,
    DB_SESSION: Annotated[Session, Depends(db_service.get_db_session)],
) -> JSONResponse:
    """
    This route handles a bulk mobile data purchase request.
    """

    logging.info("Received a bulk mobile data purchase request")

    response: JSONResponse = await handle_bulk_mobile_upload_purchase_request(
        csv_path, DB_SESSION
    )

    logging.info("Successfully completed the bulk mobile data purchase request")

    return response
