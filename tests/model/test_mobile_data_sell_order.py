import pytest
from pydantic import ValidationError
from app.model.mobile_data_sell_order import MobileDataSellOrder


def test_parse_date_of_birth():
    date_of_birth_str = "01/01/1990"
    parsed_date = MobileDataSellOrder.parse_date_of_birth(date_of_birth_str)
    assert parsed_date.year == 1990
    assert parsed_date.month == 1
    assert parsed_date.day == 1


def test_parse_date_of_birth_invalid_format():
    invalid_date_of_birth_str = "1990-01-01"
    with pytest.raises(ValueError):
        MobileDataSellOrder.parse_date_of_birth(invalid_date_of_birth_str)


def test_parse_credit_card_expiration_date():
    expiration_date_str = "12/25"
    parsed_date = MobileDataSellOrder.parse_credit_card_expiration(expiration_date_str)
    assert parsed_date.year == 2025
    assert parsed_date.month == 12


def test_parse_credit_card_expiration_date_invalid_format():
    invalid_expiration_date_str = "2025-12"
    with pytest.raises(ValueError):
        MobileDataSellOrder.parse_credit_card_expiration(invalid_expiration_date_str)


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


def test_build_mobile_data_sell_order_from_list_missing_name():
    customer_info_missing_name = [
        "01/01/1990",
        "1234567890123456",
        "12/25",
        "123",
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


def test_build_mobile_data_sell_order_from_list_invalid_date_of_birth():
    customer_info_invalid_dob = [
        "John Doe",
        "invalid_date",
        "1234567890123456",
        "12/25",
        "123",
        "9876543210",
        "5GB",
        "Approved",
        [],
    ]

    with pytest.raises(ValidationError) as exc_info:
        MobileDataSellOrder.build_mobile_data_sell_order_from_list(
            customer_info_invalid_dob
        )

    error_message = str(exc_info.value)
    assert "date_of_birth" in error_message
