"""
This module contains functions that handle API requests. The functions in this module are called by
the FastAPI routes defined in main.py. The functions in this module build a request from a binary
file, process the request, and return a JSON response with the status and BAN of the request.

Methods:
    - handle_single_mobile_data_purchase_request
"""

import logging
from fastapi.responses import JSONResponse
from fastapi import Request
from app.model.customer_information import CustomerInformation
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.utils import parse_csv_rows_into_lists
from app.service.validation_service import validate_customer_information
from app.service.db_service import DataBaseService
from app.service.invoice_generation_service import generate_pdf_invoice

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


async def handle_single_mobile_data_purchase_request(
    api_request: Request, db_session: Session
) -> JSONResponse:
    """
    This function handles a single mobile data purchase request. It builds a request from a
    binary file, processes the request, and returns a JSON response with the status and BAN of the
    request.
    """
    try:

        logger.info("Splitting bulk customer information into lists")

        lists_of_customer_information: list[list[str]] = (
            await parse_csv_rows_into_lists(await api_request.body())
        )

        responses: dict = {}

        for single_customer_information_list in lists_of_customer_information:
            logger.info("Building customer information object")

            customer_information: CustomerInformation = (
                await CustomerInformation.construct_customer_information_object_from_list(
                    single_customer_information_list
                )
            )

            logger.info("Validating customer information")
            customer_information.validation_errors += validate_customer_information(
                customer_information.date_of_birth,
                customer_information.credit_card_number,
                customer_information.credit_card_expiration_date,
                customer_information.credit_card_cvv,
            )

            customer_information.update_status()

            logger.info("Recording transaction in the database")
            DataBaseService.record_transaction(customer_information, db_session)

            logger.info("Generating PDF invoice")
            generate_pdf_invoice(customer_information)

            responses[
                f"Status for BAN {customer_information.billing_account_number}"
            ] = customer_information.status

        return JSONResponse(content=responses)

    except Exception as e:
        print(e)
        logger.error("Failed to process the mobile data purchase request")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error: Failed to process the mobile data purchase request",
        )
