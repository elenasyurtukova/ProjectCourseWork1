import logging

from config import PATH_TO_LOGGER


def get_logger(filename: str) -> logging.Logger:
    """Получение логера для записи логов в файл"""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s",
        filename=PATH_TO_LOGGER / filename,
        encoding="UTF-8",
        filemode="w",
    )
    logger = logging.getLogger(__name__)
    return logger
