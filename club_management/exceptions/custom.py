class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str
    ):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            status_code=404,
            message=message,
            error_code="NOT_FOUND"
        )


class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(
            status_code=400,
            message=message,
            error_code="BAD_REQUEST"
        )


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            status_code=401,
            message=message,
            error_code="UNAUTHORIZED"
        )


class ConflictException(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(
            status_code=409,
            message=message,
            error_code="CONFLICT"
        )

class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            status_code=403,
            message=message,
            error_code="FORBIDDEN"
        )

class ServiceUnavailableException(AppException):
    def __init__(self, message: str = "Service unavailable"):
        super().__init__(
            status_code=503,
            message=message,
            error_code="SERVICE_UNAVAILABLE"
        )

class TooManyRequestsException(AppException):
    def __init__(self, message: str = "Too many requests"):
        super().__init__(
            status_code=429,
            message=message,
            error_code="TOO_MANY_REQUESTS"
        )

class UnsupportedMediaTypeException(AppException):
    def __init__(self, message: str = "Unsupported file type"):
        super().__init__(
            status_code=415,
            message=message,
            error_code="UNSUPPORTED_MEDIA_TYPE"
        )

class PayloadTooLargeException(AppException):
    def __init__(self, message: str = "File too large"):
        super().__init__(
            status_code=413,
            message=message,
            error_code="PAYLOAD_TOO_LARGE"
        )