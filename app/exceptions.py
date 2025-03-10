# Custom Exception Classes
class UnderageException(Exception):
    """Raised when a customer is not of legal age."""

    pass


class InvalidCreditCardLengthException(Exception):
    """Raised when the credit card number length is invalid."""

    pass


class InvalidCreditCardNumberException(Exception):
    """Raised when the credit card number is invalid (fails Luhn check)."""

    pass


class InvalidCVVException(Exception):
    """Raised when the CVV length is invalid."""

    pass


class CreditCardExpiredException(Exception):
    """Raised when the credit card expiration date has passed."""

    pass
