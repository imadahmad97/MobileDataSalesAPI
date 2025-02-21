"""
This module contains the functions that validate a purchase request. It checks if the customer is
of legal age, if the credit card number is valid, if the credit card number length is valid, if the
credit card cvv is valid, and if the credit card expiration date is valid. It returns a string of
validation errors.

Dependencies:
    - datetime
    - luhncheck.is_luhn
    - os
    - logging
    
Methods:
    - validate_purchase_request
    - is_customer_of_legal_age
    - is_credit_card_number_length_valid
    - is_credit_card_number_valid
    - is_cvv_valid
    - is_credit_card_expired
"""

import os
import datetime
import logging
from luhncheck import is_luhn


def validate_purchase_request(
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
    logging.info("Initializing the purchase request validation process")
    # Prep Step: Initialize validation errors list
    validation_errors: str = ""

    # Prep Step: Load environment variables
    minimum_card_number_length: int = int(
        os.getenv("MINIMUM_CREDIT_CARD_NUMBER_LENGTH", "15")
    )
    maximum_card_number_length: int = int(
        os.getenv("MAXIMUM_CREDIT_CARD_NUMBER_LENGTH", "19")
    )
    minimum_cvv_length: int = int(os.getenv("MINIMUM_CVV_LENGTH", "3"))
    maximum_cvv_length: int = int(os.getenv("MAXIMUM_CVV_LENGTH", "4"))
    legal_age: int = int(os.getenv("LEGAL_AGE", "18"))

    logging.info("Validating the customer is of legal age")
    # Step 1: Validate that the requestor is of legal age
    validation_errors += is_customer_of_legal_age(date_of_birth, legal_age)

    logging.info("Validating the credit card number length")
    # Step 2: Validate the credit card number length
    validation_errors += is_credit_card_number_length_valid(
        credit_card_number, minimum_card_number_length, maximum_card_number_length
    )

    logging.info("Validating the credit card number")
    # Step 3: Validate the credit card number
    validation_errors += is_credit_card_number_valid(credit_card_number)

    logging.info("Validating the credit card cvv")
    # Step 4: Validate the credit card cvv
    validation_errors += is_cvv_valid(
        credit_card_cvv, minimum_cvv_length, maximum_cvv_length
    )

    logging.info("Validating the credit card expiration date")
    # Step 5: Validate the credit card expiration date
    validation_errors += is_credit_card_expired(credit_card_expiration_date)

    # Return the validation errors
    return validation_errors


def is_customer_of_legal_age(date_of_birth: datetime.datetime, legal_age: int) -> str:
    """
    This function checks if the customer is of legal age.
    """
    age: float = (datetime.datetime.now() - date_of_birth).days / 365.2425
    if age >= legal_age:
        return ""
    return "Customer is not of legal age. "


def is_credit_card_number_length_valid(
    credit_card_number: str,
    minimum_card_number_length: int,
    maximum_card_number_length: int,
) -> str:
    """
    This function checks if the credit card number length is between the provided minimum and
    maximum.
    """
    if (
        minimum_card_number_length
        <= len(credit_card_number)
        <= maximum_card_number_length
    ):
        return ""
    return "Credit card number is invalid. "


def is_credit_card_number_valid(
    credit_card_number: str,
) -> str:
    """
    This function checks if the credit card number is valid using the Luhn algorithm.
    """
    if is_luhn(credit_card_number):
        return ""
    return "Credit card number is invalid. "


def is_cvv_valid(
    credit_card_cvv: str, minimum_cvv_length: int, maximum_cvv_length: int
) -> str:
    """
    This function checks if the credit card cvv length is between the provided minimum and maximum.
    """
    if minimum_cvv_length <= len(credit_card_cvv) <= maximum_cvv_length:
        return ""
    return "CVV is invalid. "


def is_credit_card_expired(credit_card_expiration_date: datetime.datetime) -> str:
    """
    This function checks if the credit card expiration date is in the future.
    """
    if credit_card_expiration_date >= datetime.datetime.now():
        return ""
    return "Credit card is expired. "
