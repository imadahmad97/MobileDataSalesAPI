"""
This module contains the validation functions used to validate the customer's information. These
functions are used by the validation_interface module to validate the customer's information.
"""

import datetime


class CreditRequestValidator:
    def __init__(
        self,
        legal_age,
        minimum_card_number_length,
        maximum_card_number_length,
        minimum_cvv_length,
        maximum_cvv_length,
        days_in_year,
        luhn_validator,
    ):
        self.legal_age = legal_age
        self.minimum_card_number_length = minimum_card_number_length
        self.maximum_card_number_length = maximum_card_number_length
        self.minimum_cvv_length = minimum_cvv_length
        self.maximum_cvv_length = maximum_cvv_length
        self.days_in_year = days_in_year
        self.luhn_validator = luhn_validator

    def is_customer_of_legal_age(self, date_of_birth: datetime.datetime) -> bool:
        """
        This function checks if the customer is of legal age.

        Args:
            date_of_birth (datetime.datetime): The date of birth of the customer.
        """
        age: int = datetime.datetime.now().year - date_of_birth.year
        if date_of_birth.month > datetime.datetime.now().month:
            age -= 1
        elif date_of_birth.month == datetime.datetime.now().month:
            if date_of_birth.day > datetime.datetime.now().day:
                age -= 1

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

        Args:
            credit_card_number (str): The credit card number to be validated.
        """
        if not (
            self.minimum_card_number_length
            <= len(credit_card_number)
            <= self.maximum_card_number_length
        ):
            return False
        return True

    def is_credit_card_number_valid(
        self,
        credit_card_number: str,
    ) -> bool:
        """
        This function checks if the credit card number is valid using the Luhn algorithm.

        Args:
            credit_card_number (str): The credit card number to be validated.
        """
        if not self.luhn_validator(credit_card_number):
            return False
        return True

    def is_cvv_valid(self, credit_card_cvv: str) -> bool:
        """
        This function checks if the credit card cvv length is between the provided minimum and maximum.

        Args:
            credit_card_cvv (str): The credit card cvv to be validated.
        """
        if (
            not self.minimum_cvv_length
            <= len(credit_card_cvv)
            <= self.maximum_cvv_length
        ):
            return False
        return True

    def is_credit_card_expired(
        self, credit_card_expiration_date: datetime.datetime
    ) -> bool:
        """
        This function checks if the credit card expiration date is in the future.

        Args:
            credit_card_expiration_date (datetime.datetime): The credit card expiration date to be validated.
        """
        if credit_card_expiration_date <= datetime.datetime.now():
            return False
        return True
