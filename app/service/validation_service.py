"""
This module contains the functions that validate a purchase request. It checks if the customer is
of legal age, if the credit card number is valid, if the credit card number length is valid, if the
credit card cvv is valid, and if the credit card expiration date is valid. It returns a string of
validation errors.
"""

import os
import datetime
import logging
from fastapi import HTTPException
from luhncheck import is_luhn
from exceptions import (
    UnderageException,
    InvalidCreditCardLengthException,
    InvalidCreditCardNumberException,
    InvalidCVVException,
    CreditCardExpiredException,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def validate_mobile_sell_order(
    date_of_birth: datetime.datetime,
    credit_card_number: str,
    credit_card_expiration_date: datetime.datetime,
    credit_card_cvv: str,
) -> str:
    """
    This function validates a purchase request. It checks if the customer is of legal age, if the
    credit card number is valid, if the credit card number length is valid, if the credit card cvv
    is valid, and if the credit card expiration date is valid. It returns a string of validation
    errors.
    """
    # Step 1: Validate that the requestor is of legal age
    logger.info("Validating the customer is of legal age")
    try:
        is_customer_of_legal_age(date_of_birth, int(os.getenv("LEGAL_AGE", "18")))
    except UnderageException as e:
        

    logger.info("Validating the credit card number length")
    # Step 2: Validate the credit card number length
    validation_errors += is_credit_card_number_length_valid(
        credit_card_number, minimum_card_number_length, maximum_card_number_length
    )

    logger.info("Validating the credit card number")
    # Step 3: Validate the credit card number
    validation_errors += is_credit_card_number_valid(credit_card_number)

    logger.info("Validating the credit card cvv")
    # Step 4: Validate the credit card cvv
    validation_errors += is_cvv_valid(
        credit_card_cvv, minimum_cvv_length, maximum_cvv_length
    )

    logger.info("Validating the credit card expiration date")
    # Step 5: Validate the credit card expiration date
    validation_errors += is_credit_card_expired(credit_card_expiration_date)

    # Return the validation errors
    return validation_errors


def is_customer_of_legal_age(date_of_birth: datetime.datetime, legal_age: int) -> None:
    """
    This function checks if the customer is of legal age.
    """
    age: float = (datetime.datetime.now() - date_of_birth).days / 365.2425
    if age < legal_age:
        raise UnderageException("Customer is not of legal age.")
    return None


def is_credit_card_number_length_valid(
    credit_card_number: str,
    minimum_card_number_length: int,
    maximum_card_number_length: int,
) -> None:
    """
    This function checks if the credit card number length is between the provided minimum and
    maximum.
    """
    if not (
        minimum_card_number_length
        <= len(credit_card_number)
        <= maximum_card_number_length
    ):
        raise InvalidCreditCardLengthException("Credit card number length is invalid.")
    return None


def is_credit_card_number_valid(
    credit_card_number: str,
) -> None:
    """
    This function checks if the credit card number is valid using the Luhn algorithm.
    """
    if not is_luhn(credit_card_number):
        raise InvalidCreditCardNumberException("Credit card number is invalid.")
    return None


def is_cvv_valid(
    credit_card_cvv: str, minimum_cvv_length: int, maximum_cvv_length: int
) -> None:
    """
    This function checks if the credit card cvv length is between the provided minimum and maximum.
    """
    if not minimum_cvv_length <= len(credit_card_cvv) <= maximum_cvv_length:
        raise InvalidCVVException("CVV length is invalid.")
    return None


def is_credit_card_expired(credit_card_expiration_date: datetime.datetime) -> None:
    """
    This function checks if the credit card expiration date is in the future.
    """
    if credit_card_expiration_date < datetime.datetime.now():
        raise CreditCardExpiredException("Credit card has expired.")
    return None
