import pytest
from pydantic import ValidationError
from app.model.mobile_data_sell_order import MobileDataSellOrder


def test_build_mobile_data_sell_order_from_list():
    customer_info = [
        "John Doe",
        "01/01/1990",
        "1234567890123456",
        "12/25",
        "123",
        "9876543210",
        "5GB",
        "Approved",
        [],
    ]

    customer_info_result = MobileDataSellOrder.build_mobile_data_sell_order_from_list(
        customer_info
    )

    customer_info_expected_result = MobileDataSellOrder(
        name="John Doe",
        date_of_birth="01/01/1990",
        credit_card_number="1234567890123456",
        credit_card_expiration_date="12/25",
        credit_card_cvv="123",
        billing_account_number="9876543210",
        requested_mobile_data="5GB",
        status="Approved",
        validation_errors=[],
    )

    assert customer_info_result == customer_info_expected_result


def test_build_mobile_data_sell_order_from_list_missing_name_raises():
    customer_info_missing_name = [
        "01/01/1990",  # should be name
        "1234567890123456",  # wrong type for date_of_birth
        "12/25",  # wrong type for credit_card_number
        "123",  # wrong format for expiration
        "9876543210",
        "5GB",
        "Approved",
        [],
    ]

    with pytest.raises(ValidationError) as exc_info:
        MobileDataSellOrder.build_mobile_data_sell_order_from_list(
            customer_info_missing_name
        )

    error_message = str(exc_info.value)
    assert "date_of_birth" in error_message
    assert "credit_card_expiration_date" in error_message
