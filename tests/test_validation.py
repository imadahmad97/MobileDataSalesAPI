from app.validation.validator import Validator
import config
from luhncheck import is_luhn
import datetime
from unittest import mock

validator = Validator(
    config.LEGAL_AGE,
    config.MINIMUM_CARD_NUMBER_LENGTH,
    config.MAXIMUM_CARD_NUMBER_LENGTH,
    config.MINIMUM_CVV_LENGTH,
    config.MAXIMUM_CVV_LENGTH,
    config.DAYS_IN_YEAR,
    is_luhn,
)


@mock.patch("app.validation.validator.datetime")
def test_is_customer_of_legal_age(mock_datetime):
    mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 1, 0, 0, 0)

    assert validator.is_customer_of_legal_age(
        datetime.datetime(2004, 10, 1, 0, 0, 0)
    )  # 19 years old
    assert validator.is_customer_of_legal_age(
        datetime.datetime(2005, 10, 1, 0, 0, 0)
    )  # 18 years old
    assert validator.is_customer_of_legal_age(
        datetime.datetime(2004, 9, 30, 0, 0, 0)
    )  # One day after 18 years old
    assert not validator.is_customer_of_legal_age(
        datetime.datetime(2006, 10, 1, 0, 0, 0)
    )  # 17 years old
    assert not validator.is_customer_of_legal_age(
        datetime.datetime(2005, 10, 2, 0, 0, 0)
    )  # One day before 18 years old


def test_is_credit_card_number_length_valid():
    assert validator.is_credit_card_number_length_valid("1234567890123456")  # Length 16
    assert validator.is_credit_card_number_length_valid("123456789012345")  # Length 15
    assert validator.is_credit_card_number_length_valid("1234567890123")  # Length 13
    assert validator.is_credit_card_number_length_valid(
        "1234567890123456789"
    )  # Length 19
    assert not validator.is_credit_card_number_length_valid("123456789111")  # Length 12
    assert not validator.is_credit_card_number_length_valid(
        "1234567890123456789012"
    )  # Length 20


def test_is_credit_card_number_valid():
    assert validator.is_credit_card_number_valid("2222405343248877")  # Valid Luhn
    assert validator.is_credit_card_number_valid("5105105105105100")  # Valid Luhn
    assert not validator.is_credit_card_number_valid("1234567890123456")  # Invalid Luhn
    assert not validator.is_credit_card_number_valid("123456789012345")  # Invalid Luhn


def test_is_cvv_valid():
    assert validator.is_cvv_valid("123")  # Valid CVV length
    assert validator.is_cvv_valid("1234")  # Valid CVV length
    assert not validator.is_cvv_valid("12")  # Invalid CVV length
    assert not validator.is_cvv_valid("12345")  # Invalid CVV length


@mock.patch("app.validation.validator.datetime")
def test_is_credit_card_expired(mock_datetime):
    mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 1, 0, 0, 0)

    assert validator.is_credit_card_expired(datetime.datetime(2024, 10, 1, 0, 0, 0))
    assert validator.is_credit_card_expired(datetime.datetime(2023, 11, 1, 0, 0, 0))
    assert not validator.is_credit_card_expired(datetime.datetime(2023, 9, 1, 0, 0, 0))
    assert not validator.is_credit_card_expired(datetime.datetime(2023, 10, 1, 0, 0, 0))
