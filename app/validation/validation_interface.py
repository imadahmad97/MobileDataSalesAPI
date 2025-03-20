"""
This module contains the interface for the validation functions. It includes a function to validate
a list of mobile data sell orders and a function to validate a single mobile data sell order.
"""

import logging
from app.validation.validation_functions import Validation
from app.model.mobile_data_sell_order import MobileDataSellOrder

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def validate_sell_orders(
    sell_orders: list[MobileDataSellOrder],
):
    """
    This function validates a list of mobile data sell orders.
    """
    for sell_order in sell_orders:
        logger.info(
            f"Validating mobile data sell order for BAN: {sell_order.billing_account_number}"
        )
        validate_sell_order(sell_order)


def validate_sell_order(
    sell_order: MobileDataSellOrder,
) -> None:
    """
    This function validates a single mobile data sell order. It does so by calling the individual
    validation functions and appending any errors to the validation_errors attribute of the
    MobileDataSellOrder object.
    """
    errors: list[str] = []

    # Step 1: Validate that the requestor is of legal age
    logger.info("Validating the customer is of legal age")
    if not Validation.is_customer_of_legal_age(sell_order.date_of_birth):
        errors.append("Customer is not of legal age")

    # Step 2: Validate the credit card number length
    logger.info("Validating the credit card number length")
    if not Validation.is_credit_card_number_length_valid(
        sell_order.credit_card_number,
    ):
        errors.append("Credit card number length is invalid")

    # Step 3: Validate the credit card number
    logger.info("Validating the credit card number")
    if not Validation.is_credit_card_number_valid(sell_order.credit_card_number):
        errors.append("Credit card number is invalid")

    # Step 4: Validate the credit card cvv
    logger.info("Validating the credit card cvv")
    if not Validation.is_cvv_valid(
        sell_order.credit_card_cvv,
    ):
        errors.append("CVV length is invalid")

    # Step 5: Validate the credit card expiration date
    logger.info("Validating the credit card expiration date")
    if not Validation.is_credit_card_expired(sell_order.credit_card_expiration_date):
        errors.append("Credit card has expired")

    # Step 6: Raise an exception if there are any validation errors
    if errors:
        logger.error("Rejecting due to validation errors: %s", errors)
        sell_order.validation_errors = errors
        sell_order.status = "Rejected"
