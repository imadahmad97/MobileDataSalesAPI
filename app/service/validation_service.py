"""
This module contains the functions that validate a purchase request. It checks if the customer is
of legal age, if the credit card number is valid, if the credit card number length is valid, if the
credit card cvv is valid, and if the credit card expiration date is valid, and raises exceptions if
any of the validations fail.
"""

import os
import datetime
import logging
from luhncheck import is_luhn
from app.exceptions import (
    UnderageException,
    InvalidCreditCardLengthException,
    InvalidCreditCardNumberException,
    InvalidCVVException,
    CreditCardExpiredException,
    ValidationError,
)
from app.model.mobile_data_sell_order import MobileDataSellOrder

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def validate_mobile_data_sell_orders(
    mobile_data_sell_orders: list[MobileDataSellOrder],
):
    for mobile_data_sell_order in mobile_data_sell_orders:
        validate_mobile_data_sell_order(mobile_data_sell_order)


def validate_mobile_data_sell_order(
    mobile_data_sell_order: MobileDataSellOrder,
) -> None:
    """
    This function validates a purchase request. It checks if the customer is of legal age, if the
    credit card number is valid, if the credit card number length is valid, if the credit card cvv
    is valid, and if the credit card expiration date is valid. It returns a string of validation
    errors.
    """
    errors: list[str] = []

    # Step 1: Validate that the requestor is of legal age
    logger.info("Validating the customer is of legal age")
    try:
        is_customer_of_legal_age(
            mobile_data_sell_order.date_of_birth, int(os.getenv("LEGAL_AGE", "18"))
        )
    except UnderageException as e:
        errors.append(str(e))
        logger.error(str(e))

    # Step 2: Validate the credit card number length
    logger.info("Validating the credit card number length")
    try:
        is_credit_card_number_length_valid(
            mobile_data_sell_order.credit_card_number,
            int(os.getenv("MINIMUM_CARD_NUMBER_LENGTH", "14")),
            int(os.getenv("MAXIMUM_CARD_NUMBER_LENGTH", "19")),
        )
    except InvalidCreditCardLengthException as e:
        errors.append(str(e))
        logger.error(str(e))

    # Step 3: Validate the credit card number
    logger.info("Validating the credit card number")
    try:
        is_credit_card_number_valid(mobile_data_sell_order.credit_card_number)
    except InvalidCreditCardNumberException as e:
        errors.append(str(e))
        logger.error(str(e))

    # Step 4: Validate the credit card cvv
    logger.info("Validating the credit card cvv")
    try:
        is_cvv_valid(
            mobile_data_sell_order.credit_card_cvv,
            int(os.getenv("MINIMUM_CVV_LENGTH", "3")),
            int(os.getenv("MAXIMUM_CVV_LENGTH", "4")),
        )
    except InvalidCVVException as e:
        errors.append(str(e))
        logger.error(str(e))

    # Step 5: Validate the credit card expiration date
    logger.info("Validating the credit card expiration date")
    try:
        is_credit_card_expired(mobile_data_sell_order.credit_card_expiration_date)
    except CreditCardExpiredException as e:
        errors.append(str(e))
        logger.error(str(e))

    # Step 6: Raise an exception if there are any validation errors
    if errors:
        logger.error("Rejecting due to validation errors: %s", errors)
        mobile_data_sell_order.validation_errors = errors
        mobile_data_sell_order.status = "Rejected"


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
