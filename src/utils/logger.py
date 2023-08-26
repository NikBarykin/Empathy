import logging


def create_logger(stage_name: str) -> logging.Logger:
    """Create logger for a stage with 'stage_name'"""
    logger = logging.getLogger(stage_name)

    # handler
    handler = logging.FileHandler("stages.log")

    # formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
