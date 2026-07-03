import logging


def log_side_effect_failure(
    logger: logging.Logger,
    action: str,
    exc: Exception,
    **context: object,
) -> None:
    logger.warning("%s failed: %s | context=%s", action, exc, context)
