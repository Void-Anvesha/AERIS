class AERISException(Exception):
    """Base exception for AERIS application errors."""


class NotFoundError(AERISException):
    pass


class ValidationError(AERISException):
    pass
