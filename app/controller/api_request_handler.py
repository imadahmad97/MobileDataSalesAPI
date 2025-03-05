"""
This module contains functions that handle API requests. The functions in this module are called by
the FastAPI routes defined in main.py. The functions in this module build a request from a binary
file, process the request, and return a JSON response with the status and BAN of the request.
"""

import io
import csv
import logging
from sqlalchemy.orm import Session
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.service.db_service import DataBaseService
from app.model.customer_information import CustomerInformation
from app.service.invoice_generation_service import generate_pdf_invoice
from app.service.validation_service import validate_customer_information

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


async def handle_mobile_data_purchase_request(
    api_request: Request, db_session: Session
) -> JSONResponse:
    """
    This function handles a mobile data purchase request. It takes a request as input, processes the
    request into multiple sets of customer information, validates the customer information, records
    the transaction in the database, generates a PDF invoice, and returns a JSON response with the
    status and BAN of each request.
    """

    try:

        logger.info("Splitting bulk customer information into lists")

        customer_data_rows: list[list[str]] = await parse_csv_rows_into_lists(
            await api_request.body()
        )

        responses: dict = {}

        for customer_data_row in customer_data_rows:
            logger.info("Building customer information object")

            customer_information: CustomerInformation = (
                await CustomerInformation.construct_customer_information_object_from_list(
                    customer_data_row
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

    except Exception:
        logger.error("Failed to process the mobile data purchase request")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error: Failed to process the mobile data purchase request",
        )


async def parse_csv_rows_into_lists(contents: bytes) -> list[list[str]]:
    """
    Parses the contents of a csv file into a list of rows, where each row is a list of strings.
    """
    csv_text: io.StringIO = io.StringIO(contents.decode("utf-8"))
    reader: csv.reader = csv.reader(csv_text)
    parsed_rows: list[list[str]] = list(reader)

    return parsed_rows
