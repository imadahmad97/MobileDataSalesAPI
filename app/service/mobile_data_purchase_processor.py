from app.model.mobile_data_purchase_request import MobileDataPurchaseRequest
from app.model.mobile_data_purchase_response import MobileDataPurchaseResponse
from app.interface.validation_interface import validate_purchase_request
from app.service.invoice_generation_service import generate_pdf
import datetime


async def process_mobile_data_purchase_request(
    mobile_data_purchase_request, db_service
):
    # Prep Step: Initialize a new mobile data purchase request object:
    purchase_request = await MobileDataPurchaseRequest.from_binary_data(
        mobile_data_purchase_request
    )

    # Prep Step: Initialize a new mobile data purchase response object:
    purchase_response = MobileDataPurchaseResponse(
        name=purchase_request.name,
        credit_card_number=purchase_request.credit_card_number,
        billing_account_number=purchase_request.billing_account_number,
        requested_mobile_data=purchase_request.requested_mobile_data,
        status="",
        validation_errors="",
    )

    # Step 1: Validate the purchase request and append any validation errors to the response object
    purchase_response.validation_errors += validate_purchase_request(
        purchase_request.date_of_birth,
        purchase_request.credit_card_number,
        purchase_request.credit_card_expiration_date,
        purchase_request.credit_card_cvv,
    )

    # Step 2: Approve the purchase request if there are no validation errors
    if not purchase_response.validation_errors:
        purchase_response.status = "Approved"
    else:
        purchase_response.status = "Rejected"

    # Step 3: Save the purchase request to the database
    db_service.record_transaction(
        purchase_request.name,
        purchase_request.date_of_birth,
        purchase_request.credit_card_number,
        purchase_request.credit_card_expiration_date,
        purchase_request.credit_card_cvv,
        purchase_request.billing_account_number,
        purchase_request.requested_mobile_data,
        purchase_response.status,
        purchase_response.validation_errors,
    )

    # Step 3: Generate a PDF invoice for the purchase request
    pdf = generate_pdf(
        purchase_request.name,
        purchase_request.date_of_birth,
        purchase_request.credit_card_number[:-4],
        purchase_request.credit_card_expiration_date,
        purchase_request.credit_card_cvv,
        purchase_request.billing_account_number,
        purchase_request.requested_mobile_data,
        purchase_response.status,
        purchase_response.validation_errors,
    )

    print(purchase_response.validation_errors)
