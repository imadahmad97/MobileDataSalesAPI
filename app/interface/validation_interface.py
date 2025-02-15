from luhncheck import is_luhn
import os
import datetime


def validate_purchase_request(
    date_of_birth, credit_card_number, credit_card_expiration_date
):
    # Prep Step: Initialize validation errors list
    validation_errors = ""

    # Prep Step: Load environment variables
    minimum_card_number_length = int(os.getenv("MINIMUM_CREDIT_CARD_NUMBER_LENGTH", 15))
    maximum_card_number_length = int(os.getenv("MAXIMUM_CREDIT_CARD_NUMBER_LENGTH", 19))
    legal_age = int(os.getenv("LEGAL_AGE", 18))

    # Step 1: Validate that the requestor is of legal age
    validation_errors += is_customer_of_legal_age(date_of_birth, legal_age)

    # Step 2: Validate the credit card number
    validation_errors += is_credit_card_number_valid(
        credit_card_number,
        minimum_card_number_length,
        maximum_card_number_length,
    )

    # Step 3: Validate the credit card expiration date
    validation_errors += is_credit_card_expired(credit_card_expiration_date)

    # Return the validation errors list
    return validation_errors


def is_customer_of_legal_age(date_of_birth, legal_age):
    age = (datetime.datetime.now() - date_of_birth).days / 365.2425
    if age >= legal_age:
        return ""
    else:
        return "Customer is not of legal age."


def is_credit_card_number_valid(
    credit_card_number,
    minimum_card_number_length,
    maximum_card_number_length,
):
    if (
        minimum_card_number_length
        <= len(credit_card_number)
        <= maximum_card_number_length
    ) and is_luhn(credit_card_number):
        return ""
    else:
        return "Credit card number is invalid."


def is_credit_card_expired(credit_card_expiration_date):
    if credit_card_expiration_date >= datetime.datetime.now():
        return ""
    else:
        return "Credit card is expired."
