"""
This module contains the routes for the mobile data sales API.

Routes:
    /mobile-data-purchase-request
        purchase_request: Request
            The purchase request to be processed.
        db_session: Annotated[Session, Depends(db_service.get_db_session)]
            The database session to be used for the request.

        Returns:
            JSONResponse
                The response to the purchase request.
        methods: POST
"""

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from app.service.db_service import DataBaseService
from app.controller.api_request_handler import (
    handle_mobile_data_sell_request,
)
from app.validation.validator import CreditRequestValidator
import logging
from sqlalchemy.orm import Session
from typing import Annotated
from contextlib import asynccontextmanager
import config
import qrcode  # type: ignore
from app.service.invoice_generator import InvoiceGenerator
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML  # type: ignore
from luhncheck import is_luhn

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

logger.info("Starting the FastAPI application")

logger.info("Initializing Database")
db_service = DataBaseService(config.PATH_TO_DB_FILE)
db_session = Annotated[Session, Depends(db_service.get_db_session)]

logger.info("Initializing validator")
validator = CreditRequestValidator(
    legal_age=config.LEGAL_AGE,
    minimum_card_number_length=config.MINIMUM_CARD_NUMBER_LENGTH,
    maximum_card_number_length=config.MAXIMUM_CARD_NUMBER_LENGTH,
    minimum_cvv_length=config.MINIMUM_CVV_LENGTH,
    maximum_cvv_length=config.MAXIMUM_CVV_LENGTH,
    days_in_year=config.DAYS_IN_YEAR,
    luhn_validator=is_luhn,
)

logger.info("Initializing invoice generator")
invoice_generator = InvoiceGenerator(
    invoice_template_path=config.INVOICE_TEMPLATE_PATH,
    pdf_output_path=config.PDF_OUTPUT_PATH,
    qr_code_base_url=config.QR_CODE_BASE_URL,
    qr_code_template=qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=2,
    ),
    html_template=config.HTML_TEMPLATE,
    html_template_environment=Environment(
        loader=FileSystemLoader(config.INVOICE_TEMPLATE_PATH),
    ),
    html_factory=lambda s: HTML(string=s),
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This context manager initializes the database and tables when the FastAPI application is started
    and closes the database connection when the FastAPI application is stopped.
    """
    logger.info("Initializing the database and tables")
    db_service.create_db_and_tables()
    yield
    db_service.close_db_connection()


app: FastAPI = FastAPI(lifespan=lifespan)


@app.post("/mobile-data-purchase-request")
async def mobile_data_purchase_request_route(
    purchase_request: Request,
    db_session: Annotated[Session, Depends(db_service.get_db_session)],
) -> JSONResponse:
    """
    This route handles a mobile data purchase request. It takes a purchase request as input and
    feeds it to the handle_mobile_data_purchase_request function. The function processes the route
    and returns a JSON response.
    """

    logger.info("Received a mobile data purchase request")

    response: JSONResponse = await handle_mobile_data_sell_request(
        purchase_request, db_session, validator, invoice_generator
    )

    logger.info("Successfully completed the mobile data purchase request")

    return response
