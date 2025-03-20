"""
This module contains the interface for the validation functions. It includes a function to validate
a list of mobile data sell orders and a function to validate a single mobile data sell order.
"""

import os
import logging
from app.validation.validation_functions import Validation
from app.validation.exceptions import (
    UnderageException,
    InvalidCreditCardLengthException,
    InvalidCreditCardNumberException,
    InvalidCVVException,
    CreditCardExpiredException,
)
from app.model.mobile_data_sell_order import MobileDataSellOrder

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def validate_mobile_data_sell_orders(
    mobile_data_sell_orders: list[MobileDataSellOrder],
):
    """
    This function validates a list of mobile data sell orders.
    """
    for mobile_data_sell_order in mobile_data_sell_orders:
        logger.info(
            f"Validating mobile data sell order for BAN: {mobile_data_sell_order.billing_account_number}"
        )
        validate_mobile_data_sell_order(mobile_data_sell_order)


def validate_mobile_data_sell_order(
    mobile_data_sell_order: MobileDataSellOrder,
) -> None:
    """
    This function validates a single mobile data sell order. It does so by calling the individual
    validation functions and appending any errors to the validation_errors attribute of the
    MobileDataSellOrder object.
    """
    errors: list[str] = []

    # Step 1: Validate that the requestor is of legal age
    logger.info("Validating the customer is of legal age")
    try:
        Validation.is_customer_of_legal_age(mobile_data_sell_order.date_of_birth)
    except UnderageException as e:
        errors.append(str(e))
        logger.error(str(e))

    # Step 2: Validate the credit card number length
    logger.info("Validating the credit card number length")
    try:
        Validation.is_credit_card_number_length_valid(
            mobile_data_sell_order.credit_card_number,
        )
    except InvalidCreditCardLengthException as e:
        errors.append(str(e))
        logger.error(str(e))

    # Step 3: Validate the credit card number
    logger.info("Validating the credit card number")
    try:
        Validation.is_credit_card_number_valid(
            mobile_data_sell_order.credit_card_number
        )
    except InvalidCreditCardNumberException as e:
        errors.append(str(e))
        logger.error(str(e))

    # Step 4: Validate the credit card cvv
    logger.info("Validating the credit card cvv")
    try:
        Validation.is_cvv_valid(
            mobile_data_sell_order.credit_card_cvv,
        )
    except InvalidCVVException as e:
        errors.append(str(e))
        logger.error(str(e))

    # Step 5: Validate the credit card expiration date
    logger.info("Validating the credit card expiration date")
    try:
        Validation.is_credit_card_expired(
            mobile_data_sell_order.credit_card_expiration_date
        )
    except CreditCardExpiredException as e:
        errors.append(str(e))
        logger.error(str(e))

    # Step 6: Raise an exception if there are any validation errors
    if errors:
        logger.error("Rejecting due to validation errors: %s", errors)
        mobile_data_sell_order.validation_errors = errors
        mobile_data_sell_order.status = "Rejected"
