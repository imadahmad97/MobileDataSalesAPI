from app.model.mobile_data_purchase_request import MobileDataPurchaseRequest
from app.interface.validation_interface import validate_purchase_request


async def process_mobile_data_purchase_request(mobile_data_purchase_request):
    # Prep Step: Initialize a new mobile data purchase request object:
    purchase_request = await MobileDataPurchaseRequest.from_binary_data(
        mobile_data_purchase_request
    )

    # Step 1: Validate the purchase request

    # Step 2: Save the purchase request to the database

    # Step 3: Generate a PDF invoice for the purchase request

    # Return extracted values
    return {
        "name": purchase_request.name,
        "date_of_birth": purchase_request.date_of_birth,
        "credit_card_number": purchase_request.credit_card_number,
        "credit_card_expiration_date": purchase_request.credit_card_expiration_date,
        "credit_card_cvv": purchase_request.credit_card_cvv,
        "billing_account_number": purchase_request.billing_account_number,
        "requested_mobile_data": purchase_request.requested_mobile_data,
    }
