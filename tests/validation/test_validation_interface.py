from app.validation.validation_interface import (
    validate_sell_orders,
    validate_sell_order,
)
from app.validation.validator import CreditRequestValidator
from app.model.mobile_data_sell_order import MobileDataSellOrder
import config
from luhncheck import is_luhn
import datetime
from copy import deepcopy

validator = CreditRequestValidator(
    config.LEGAL_AGE,
    config.MINIMUM_CARD_NUMBER_LENGTH,
    config.MAXIMUM_CARD_NUMBER_LENGTH,
    config.MINIMUM_CVV_LENGTH,
    config.MAXIMUM_CVV_LENGTH,
    config.DAYS_IN_YEAR,
    is_luhn,
)

test_user_no_errors = MobileDataSellOrder(
    name="John Doe",
    date_of_birth=datetime.datetime(1990, 1, 1, 0, 0),
    credit_card_number="370000000000002",
    credit_card_expiration_date=datetime.datetime(2025, 12, 1, 0, 0),
    credit_card_cvv="123",
    billing_account_number="1234567890",
    requested_mobile_data="10GB",
    status="Approved",
    validation_errors=[],
)

test_user_expired_card = deepcopy(test_user_no_errors)
test_user_expired_card.credit_card_expiration_date = datetime.datetime(
    2020, 12, 1, 0, 0
)

test_user_invalid_cvv = deepcopy(test_user_no_errors)
test_user_invalid_cvv.credit_card_cvv = "12"

test_user_invalid_card_number = deepcopy(test_user_no_errors)
test_user_invalid_card_number.credit_card_number = "1234567890123456"

test_user_invalid_card_number_length = deepcopy(test_user_no_errors)
test_user_invalid_card_number_length.credit_card_number = "1234567890123456789012"

test_user_not_of_legal_age = deepcopy(test_user_no_errors)
test_user_not_of_legal_age.date_of_birth = datetime.datetime(2010, 10, 1, 0, 0)

test_user_invalid_cvv_and_card_number = deepcopy(test_user_no_errors)
test_user_invalid_cvv_and_card_number.credit_card_cvv = "12"
test_user_invalid_cvv_and_card_number.credit_card_number = "1234567890123456"

test_user_all_errors = deepcopy(test_user_no_errors)
test_user_all_errors.credit_card_expiration_date = datetime.datetime(2020, 12, 1, 0, 0)
test_user_all_errors.credit_card_cvv = "12"
test_user_all_errors.credit_card_number = "12345678901234563244654321"
test_user_all_errors.date_of_birth = datetime.datetime(2010, 10, 1, 0, 0)


def test_validate_sell_orders():
    validated_sell_orders = validate_sell_orders(
        [
            test_user_no_errors,
            test_user_expired_card,
            test_user_invalid_cvv,
            test_user_invalid_card_number,
            test_user_invalid_card_number_length,
            test_user_not_of_legal_age,
            test_user_invalid_cvv_and_card_number,
            test_user_all_errors,
        ],
        validator,
    )

    assert len(validated_sell_orders) == 8
    assert validated_sell_orders[0].status == "Approved"
    assert validated_sell_orders[0].validation_errors == []
    assert validated_sell_orders[1].status == "Rejected"
    assert validated_sell_orders[1].validation_errors == ["Credit card has expired"]
    assert validated_sell_orders[2].status == "Rejected"
    assert validated_sell_orders[2].validation_errors == ["CVV length is invalid"]
    assert validated_sell_orders[3].status == "Rejected"
    assert validated_sell_orders[3].validation_errors == [
        "Credit card number is invalid"
    ]
    assert validated_sell_orders[4].status == "Rejected"
    assert validated_sell_orders[4].validation_errors == [
        "Credit card number length is invalid"
    ]
    assert validated_sell_orders[5].status == "Rejected"
    assert validated_sell_orders[5].validation_errors == [
        "Customer is not of legal age"
    ]
    assert validated_sell_orders[6].status == "Rejected"
    assert validated_sell_orders[6].validation_errors == [
        "Credit card number is invalid",
        "CVV length is invalid",
    ]

    assert validated_sell_orders[7].status == "Rejected"
    assert validated_sell_orders[7].validation_errors == [
        "Customer is not of legal age",
        "Credit card number length is invalid",
        "Credit card number is invalid",
        "CVV length is invalid",
        "Credit card has expired",
    ]


def test_validate_sell_order():
    assert validate_sell_order(test_user_no_errors, validator).status == "Approved"
    assert validate_sell_order(test_user_no_errors, validator).validation_errors == []

    assert validate_sell_order(test_user_expired_card, validator).status == "Rejected"
    assert validate_sell_order(test_user_expired_card, validator).validation_errors == [
        "Credit card has expired"
    ]

    assert validate_sell_order(test_user_invalid_cvv, validator).status == "Rejected"
    assert validate_sell_order(test_user_invalid_cvv, validator).validation_errors == [
        "CVV length is invalid"
    ]

    assert (
        validate_sell_order(test_user_invalid_card_number, validator).status
        == "Rejected"
    )
    assert validate_sell_order(
        test_user_invalid_card_number, validator
    ).validation_errors == ["Credit card number is invalid"]

    assert (
        validate_sell_order(test_user_invalid_card_number_length, validator).status
        == "Rejected"
    )
    assert validate_sell_order(
        test_user_invalid_card_number_length, validator
    ).validation_errors == ["Credit card number length is invalid"]

    assert (
        validate_sell_order(test_user_not_of_legal_age, validator).status == "Rejected"
    )
    assert validate_sell_order(
        test_user_not_of_legal_age, validator
    ).validation_errors == ["Customer is not of legal age"]

    assert (
        validate_sell_order(test_user_invalid_cvv_and_card_number, validator).status
        == "Rejected"
    )
    assert validate_sell_order(
        test_user_invalid_cvv_and_card_number, validator
    ).validation_errors == [
        "Credit card number is invalid",
        "CVV length is invalid",
    ]

    assert validate_sell_order(test_user_all_errors, validator).status == "Rejected"
    assert validate_sell_order(test_user_all_errors, validator).validation_errors == [
        "Customer is not of legal age",
        "Credit card number length is invalid",
        "Credit card number is invalid",
        "CVV length is invalid",
        "Credit card has expired",
    ]
