class AppError(Exception):
    pass


class NotFoundError(AppError):
    pass


class ConflictError(AppError):
    pass


class ValidationError(AppError):
    pass


class UpstreamUnavailableError(AppError):
    pass


class UpstreamBadGatewayError(AppError):
    pass
