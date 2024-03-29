from src.config import settings


def test_logger() -> None:
    logger = settings.LOGGER
    logger.debug("test debug message", extra={"x": "hello"})
    logger.info("test info message")
    logger.warning("test warning message")
    logger.error("test error message")
    logger.critical("test critical message")
    try:
        1 / 0  # noqa: B018
    except ZeroDivisionError:
        logger.exception("test exception message")
