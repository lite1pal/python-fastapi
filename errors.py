class AppError(Exception):
    status_code = 500

    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail = detail


class NotFoundError(AppError):
    status_code = 404


class ConflictError(AppError):
    status_code = 400


class ValidationError(AppError):
    status_code = 400


class UpstreamUnavailableError(AppError):
    status_code = 503


class UpstreamBadGatewayError(AppError):
    status_code = 502
