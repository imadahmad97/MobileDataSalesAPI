from app.model.mobile_data_purchase_response import MobileDataPurchaseResponse
from app.model.mobile_data_purchase_request import MobileDataPurchaseRequest
from app.interface.validation_interface import validate_purchase_request
from app.service.invoice_generation_service import generate_pdf_invoice
from app.service.db_service import DatabaseService


async def process_mobile_data_purchase_request(
    purchase_request: MobileDataPurchaseRequest, db_service: DatabaseService
) -> MobileDataPurchaseResponse:
    # Prep Step: Initialize a new mobile data purchase response object:
    purchase_response: MobileDataPurchaseResponse = MobileDataPurchaseResponse(
        name=purchase_request.name,
        credit_card_number=purchase_request.credit_card_number,
        billing_account_number=purchase_request.billing_account_number,
        requested_mobile_data=purchase_request.requested_mobile_data,
        status="",
        validation_errors="",
    )
    # Step 1: Validate the purchase request and append any validation errors to the response object
    purchase_response.validation_errors += validate_purchase_request(
        purchase_request.date_of_birth,  # type: ignore
        purchase_request.credit_card_number,
        purchase_request.credit_card_expiration_date,  # type: ignore
        purchase_request.credit_card_cvv,
    )
    # Step 2: Approve the purchase request if there are no validation errors
    purchase_response.status = (
        "Approved" if not purchase_response.validation_errors else "Rejected"
    )

    # Step 3: Save the purchase request to the database
    db_service.record_transaction(
        purchase_request,
        purchase_response.status,
        purchase_response.validation_errors,
    )
    # Step 3: Generate a PDF invoice for the purchase request
    generate_pdf_invoice(purchase_response)

    # Return the purchase response object
    return purchase_response
