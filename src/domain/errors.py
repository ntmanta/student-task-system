"""Custom errors raised by the domain and application layers."""


class ValidationError(Exception):
    """Input data breaks a business rule."""


class NotFoundError(Exception):
    """The requested record does not exist."""


class DuplicateError(Exception):
    """A value that must be unique already exists."""