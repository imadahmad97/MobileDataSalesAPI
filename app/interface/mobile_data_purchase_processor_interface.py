"""
This module contains the interface for processing a mobile data purchase request. It contains a
function that processes a mobile data purchase request. The function validates the request, updates
the status of the request, records the request to the database, and generates a PDF invoice for the
request.

Dependencies:
    - app.model.mobile_data_purchase_response.MobileDataPurchaseResponse
    - app.model.mobile_data_purchase_request.MobileDataPurchaseRequest
    - app.interface.validation_interface.validate_purchase_request
    - app.service.invoice_generation_service.generate_pdf_invoice
    - app.service.db_service.DatabaseService
    - logging

Methods:
    - process_mobile_data_purchase_request
"""

import logging
from app.model.mobile_data_purchase_response import MobileDataPurchaseResponse
from app.model.mobile_data_purchase_request import MobileDataPurchaseRequest
from app.interface.validation_interface import validate_purchase_request
from app.service.invoice_generation_service import generate_pdf_invoice
from app.service.db_service import DatabaseService


async def process_mobile_data_purchase_request(
    purchase_request: MobileDataPurchaseRequest, db_service: DatabaseService
) -> MobileDataPurchaseResponse:
    """
    This function processes a mobile data purchase request. It validates the request, updates the
    status of the request, records the request to the database, and generates a PDF invoice for the
    request.
    """

    logging.info("Initializing a new mobile data purchase response object")
    # Prep Step: Initialize a new mobile data purchase response object:
    purchase_response: MobileDataPurchaseResponse = MobileDataPurchaseResponse(
        name=purchase_request.name,
        credit_card_number=purchase_request.credit_card_number,
        billing_account_number=purchase_request.billing_account_number,
        requested_mobile_data=purchase_request.requested_mobile_data,
        status="",
        validation_errors="",
    )

    logging.info("Validating the mobile data purchase request")
    # Step 1: Validate the purchase request and append any validation errors to the response object
    purchase_response.validation_errors += validate_purchase_request(
        purchase_request.date_of_birth,  # type: ignore
        purchase_request.credit_card_number,
        purchase_request.credit_card_expiration_date,  # type: ignore
        purchase_request.credit_card_cvv,
    )

    logging.info("Updating the status of the mobile data purchase request")
    # Step 2: Approve the purchase request if there are no validation errors
    purchase_response.update_status()

    logging.info("Recording the mobile data purchase request to the database")
    # Step 3: Save the purchase request to the database
    db_service.record_transaction(
        purchase_request,
        purchase_response.status,
        purchase_response.validation_errors,
    )

    logging.info("Generating a PDF invoice for the mobile data purchase request")
    # Step 4: Generate a PDF invoice for the purchase request
    generate_pdf_invoice(purchase_response)

    # Return the purchase response object
    return purchase_response
