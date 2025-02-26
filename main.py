"""
This module contains the routes for the mobile data sales API.
    
Routes:
    /mobile-data-purchase-request
        parameters: binary_purchase_request: Request
        methods: POST
    
    /bulk-mobile-data-purchase-request
        parameters: csv_path: str
        methods: POST
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
from contextlib import asynccontextmanager


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

db_service = DataBaseService()
DB_SESSION = Annotated[Session, Depends(db_service.get_db_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This context manager initializes the database and tables when the FastAPI application is started
    and closes the database connection when the FastAPI application is stopped.
    """
    db_service.create_db_and_tables()
    yield
    db_service.close_db_connection()


app: FastAPI = FastAPI(lifespan=lifespan)


@app.post("/mobile-data-purchase-request")
async def mobile_data_purchase_request_route(
    binary_purchase_request: Request,
    DB_SESSION: Annotated[Session, Depends(db_service.get_db_session)],
) -> JSONResponse:
    """
    This route handles a single mobile data purchase request. It takes a binary file as input and
    feeds it to the handle_single_mobile_data_purchase_request function. The function processes the
    route then returns the JSON response from the handler function.
    """

    logger.info("Received a mobile data purchase request")

    response: JSONResponse = await handle_single_mobile_data_purchase_request(
        binary_purchase_request, DB_SESSION
    )

    logger.info("Successfully completed the mobile data purchase request")

    return response


@app.post("/bulk-mobile-data-purchase-request")
async def bulk_mobile_data_purchase_request_route(
    csv_path: str,
    DB_SESSION: Annotated[Session, Depends(db_service.get_db_session)],
) -> JSONResponse:
    """
    This route handles a bulk mobile data purchase request. It takes a CSV file path as input and
    feeds it to the handle_bulk_mobile_upload_purchase_request function. The function processes the
    route then returns the JSON response from the handler function.
    """

    logger.info("Received a bulk mobile data purchase request")

    response: JSONResponse = await handle_bulk_mobile_upload_purchase_request(
        csv_path, DB_SESSION
    )

    logger.info("Successfully completed the bulk mobile data purchase request")

    return response
