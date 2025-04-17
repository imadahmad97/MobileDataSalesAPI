"""
This module contains the interface for the validation functions. It includes a function to validate
a list of mobile data sell orders and a function to validate a single mobile data sell order.
"""

import logging
from app.validation.validator import CreditRequestValidator
from app.model.mobile_data_sell_order import MobileDataSellOrder
from copy import deepcopy

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def validate_sell_orders(
    sell_orders: list[MobileDataSellOrder],
    validator: CreditRequestValidator,
) -> list[MobileDataSellOrder]:
    """
    This function validates a list of mobile data sell orders.

    Args:
        sell_orders (list[MobileDataSellOrder]): The list of mobile data sell orders to be validated.
        validator (CreditRequestValidator): The validator for validating the credit requests.
    """
    validated_sell_orders = []
    for sell_order in sell_orders:
        logger.info(
            f"Validating mobile data sell order for BAN: {sell_order.billing_account_number}"
        )
        validated_sell_orders.append(validate_sell_order(sell_order, validator))

    return validated_sell_orders


def validate_sell_order(
    sell_order: MobileDataSellOrder, validator: CreditRequestValidator
) -> MobileDataSellOrder:
    """
    This function validates a single mobile data sell order. It does so by calling the individual
    validation functions and appending any errors to the validation_errors attribute of the
    MobileDataSellOrder object.

    Args:
        sell_order (MobileDataSellOrder): The mobile data sell order to be validated.
        validator (CreditRequestValidator): The validator for validating the credit requests.
    """
    validated_sell_order = deepcopy(sell_order)

    # Step 1: Validate that the requestor is of legal age
    logger.info("Validating the customer is of legal age")
    if not validator.is_customer_of_legal_age(validated_sell_order.date_of_birth):
        validated_sell_order.validation_errors.append("Customer is not of legal age")

    # Step 2: Validate the credit card number length
    logger.info("Validating the credit card number length")
    if not validator.is_credit_card_number_length_valid(
        validated_sell_order.credit_card_number,
    ):
        validated_sell_order.validation_errors.append(
            "Credit card number length is invalid"
        )

    # Step 3: Validate the credit card number
    logger.info("Validating the credit card number")
    if not validator.is_credit_card_number_valid(
        validated_sell_order.credit_card_number
    ):
        validated_sell_order.validation_errors.append("Credit card number is invalid")

    # Step 4: Validate the credit card cvv
    logger.info("Validating the credit card cvv")
    if not validator.is_cvv_valid(
        validated_sell_order.credit_card_cvv,
    ):
        validated_sell_order.validation_errors.append("CVV length is invalid")

    # Step 5: Validate the credit card expiration date
    logger.info("Validating the credit card expiration date")
    if not validator.is_credit_card_expired(
        validated_sell_order.credit_card_expiration_date
    ):
        validated_sell_order.validation_errors.append("Credit card has expired")

    # Step 6: Set status to rejected if validation errors present
    if validated_sell_order.validation_errors:
        logger.info(
            "Rejecting due to validation errors: %s",
            validated_sell_order.validation_errors,
        )
        validated_sell_order.status = "Rejected"

    return validated_sell_order
