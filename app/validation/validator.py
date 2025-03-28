"""
This module contains the validation functions used to validate the customer's information. These
functions are used by the validation_interface module to validate the customer's information.
"""

import datetime
from luhncheck import is_luhn


# CHANGE NO STATIC METHODS
class Validator:
    def __init__(
        self,
        legal_age,
        minimum_card_number_length,
        maximum_card_number_length,
        minimum_cvv_length,
        maximum_cvv_length,
        days_in_year,  # CHANGE ADD IS_LUHN TO INSTANTIATION
    ):
        self.legal_age = legal_age
        self.minimum_card_number_length = minimum_card_number_length
        self.maximum_card_number_length = maximum_card_number_length
        self.minimum_cvv_length = minimum_cvv_length
        self.maximum_cvv_length = maximum_cvv_length
        self.days_in_year = days_in_year

    def is_customer_of_legal_age(self, date_of_birth: datetime.datetime) -> bool:
        """
        This function checks if the customer is of legal age.
        """
        age: float = (datetime.datetime.now() - date_of_birth).days / self.days_in_year
        if age < self.legal_age:
            return False
        return True

    def is_credit_card_number_length_valid(
        self,
        credit_card_number: str,
    ) -> bool:
        """
        This function checks if the credit card number length is between the provided minimum and
        maximum.
        """
        if not (
            self.minimum_card_number_length
            <= len(credit_card_number)
            <= self.maximum_card_number_length
        ):
            return False
        return True

    @staticmethod
    def is_credit_card_number_valid(
        credit_card_number: str,
    ) -> bool:
        """
        This function checks if the credit card number is valid using the Luhn algorithm.
        """
        if not is_luhn(credit_card_number):
            return False
        return True

    def is_cvv_valid(self, credit_card_cvv: str) -> bool:
        """
        This function checks if the credit card cvv length is between the provided minimum and maximum.
        """
        if (
            not self.minimum_cvv_length
            <= len(credit_card_cvv)
            <= self.maximum_cvv_length
        ):
            return False
        return True

    @staticmethod  # CHANGE PASS TIME_NOW AS ARGUMENT
    def is_credit_card_expired(credit_card_expiration_date: datetime.datetime) -> bool:
        """
        This function checks if the credit card expiration date is in the future.
        """
        if credit_card_expiration_date < datetime.datetime.now():
            return False
        return True
