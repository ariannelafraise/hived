from __future__ import annotations

import logging
import os
from datetime import datetime
from logging import Logger
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import PathConfig

logs_folder_path = PathConfig.LOGS_DIR

if logs_folder_path[-1] == "/":
    logs_folder_path = logs_folder_path[:-1]
if not Path(logs_folder_path).is_dir():
    os.mkdir(logs_folder_path)

loggers: dict[str, Logger] = {}


def _init_logger(file_name: str) -> Logger:
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG)
    if not logger.hasHandlers():
        logger.addHandler(
            RotatingFileHandler(
                f"{logs_folder_path}/{file_name}", maxBytes=10**6, backupCount=5
            )
        )
    loggers[file_name] = logger
    return logger


def _get_logger(file_name: str) -> Logger:
    if file_name not in loggers:
        return _init_logger(file_name)
    return loggers[file_name]


def info(log: str, source: str, file_name: str = "hived.log") -> None:
    logger = _get_logger(file_name)
    logger.info(f"{str(datetime.now())} | {source} | {log}")


def error_traceback(traceback: str) -> None:
    logger = _get_logger("error_traceback.log")
    logger.error(f"{str(datetime.now())} | {traceback}")
