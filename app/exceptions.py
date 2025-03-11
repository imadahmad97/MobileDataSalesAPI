class ValidationError(Exception):
    """Raised when multiple validation errors occur."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("Validation failed: " + "; ".join(errors))


class UnderageException(Exception):
    """Raised when a customer is under the legal age."""

    def __init__(self, message="Customer is not of legal age."):
        super().__init__(message)


class InvalidCreditCardLengthException(Exception):
    """Raised when the credit card number length is invalid."""

    def __init__(self, message="Credit card number length is invalid."):
        super().__init__(message)


class InvalidCreditCardNumberException(Exception):
    """Raised when the credit card number is invalid."""

    def __init__(self, message="Credit card number is invalid."):
        super().__init__(message)


class InvalidCVVException(Exception):
    """Raised when the credit card CVV is invalid."""

    def __init__(self, message="CVV length is invalid."):
        super().__init__(message)


class CreditCardExpiredException(Exception):
    """Raised when the credit card has expired."""

    def __init__(self, message="Credit card has expired."):
        super().__init__(message)
