"""
This module contains the validation functions used to validate the customer's information. These
functions are used by the validation_interface module to validate the customer's information.
"""

import datetime
from app.validation.exceptions import (
    UnderageException,
    InvalidCreditCardLengthException,
    InvalidCreditCardNumberException,
    InvalidCVVException,
    CreditCardExpiredException,
)
from luhncheck import is_luhn
import config


class Validation:
    legal_age = config.LEGAL_AGE
    minimum_card_number_length = config.MINIMUM_CARD_NUMBER_LENGTH
    maximum_card_number_length = config.MAXIMUM_CARD_NUMBER_LENGTH
    minimum_cvv_length = config.MINIMUM_CVV_LENGTH
    maximum_cvv_length = config.MAXIMUM_CVV_LENGTH

    @staticmethod
    def is_customer_of_legal_age(date_of_birth: datetime.datetime) -> None:
        """
        This function checks if the customer is of legal age.
        """
        age: float = (datetime.datetime.now() - date_of_birth).days / 365.2425
        if age < Validation.legal_age:
            raise UnderageException("Customer is not of legal age.")
        return None

    @staticmethod
    def is_credit_card_number_length_valid(
        credit_card_number: str,
    ) -> None:
        """
        This function checks if the credit card number length is between the provided minimum and
        maximum.
        """
        if not (
            Validation.minimum_card_number_length
            <= len(credit_card_number)
            <= Validation.maximum_card_number_length
        ):
            raise InvalidCreditCardLengthException(
                "Credit card number length is invalid."
            )
        return None

    @staticmethod
    def is_credit_card_number_valid(
        credit_card_number: str,
    ) -> None:
        """
        This function checks if the credit card number is valid using the Luhn algorithm.
        """
        if not is_luhn(credit_card_number):
            raise InvalidCreditCardNumberException("Credit card number is invalid.")
        return None

    @staticmethod
    def is_cvv_valid(credit_card_cvv: str) -> None:
        """
        This function checks if the credit card cvv length is between the provided minimum and maximum.
        """
        if (
            not Validation.minimum_cvv_length
            <= len(credit_card_cvv)
            <= Validation.maximum_cvv_length
        ):
            raise InvalidCVVException("CVV length is invalid.")
        return None

    @staticmethod
    def is_credit_card_expired(credit_card_expiration_date: datetime.datetime) -> None:
        """
        This function checks if the credit card expiration date is in the future.
        """
        if credit_card_expiration_date < datetime.datetime.now():
            raise CreditCardExpiredException("Credit card has expired.")
        return None
