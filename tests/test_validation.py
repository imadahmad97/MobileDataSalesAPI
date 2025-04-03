from app.validation.validator import Validator
import config
from luhncheck import is_luhn

validator = Validator(
    config.LEGAL_AGE,
    config.MINIMUM_CARD_NUMBER_LENGTH,
    config.MAXIMUM_CARD_NUMBER_LENGTH,
    config.MINIMUM_CVV_LENGTH,
    config.MAXIMUM_CVV_LENGTH,
    config.DAYS_IN_YEAR,
    is_luhn,
)


# def test_is_customer_of_legal_age():
#     pass


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
