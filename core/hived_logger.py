from __future__ import annotations

import logging
import os
from datetime import datetime
from logging import Logger
from logging.handlers import RotatingFileHandler
from pathlib import Path

from core.config import PathConfig

# Setup logs directory
logs_dir_path = PathConfig.LOGS_DIR
if logs_dir_path[-1] == "/":
    logs_dir_path = logs_dir_path[:-1]
if not Path(logs_dir_path).is_dir():
    os.mkdir(logs_dir_path)

# Maintain a list of active loggers, for lazy loading
loggers: dict[str, Logger] = {}


def _load_logger(file_name: str) -> Logger:
    """
    Initializes/loads a logger by setting its level and file handler.
    Adds it to the list of active loggers and returns it.

    Parameters:
        file_name: the log file name of the logger
    """
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG)
    if not logger.hasHandlers():
        logger.addHandler(
            RotatingFileHandler(
                f"{logs_dir_path}/{file_name}", maxBytes=10**6, backupCount=5
            )
        )
    loggers[file_name] = logger
    return logger


def _get_logger(file_name: str) -> Logger:
    """
    Returns the logger associated with the file name. If it is not loaded
    into the active loggers list, initialize/load it first.

    Parameters:
        file_name: the log file's name associated with the logger. Each logger
        is associated to exactly one log file.
    """
    if file_name not in loggers:
        return _load_logger(file_name)
    return loggers[file_name]


def info(log: str, source: str, file_name: str = "hived.log") -> None:
    """
    INFO level log for a given log file.

    Parameters:
        log: the log to be sent
        source: the source of the log. for example: the name
        of the class that called this function
        file_name: the name of the log file to use
    """
    logger = _get_logger(file_name)
    logger.info(f"{str(datetime.now())} | {source} | {log}")


def error_traceback(traceback: str) -> None:
    """
    Logs a python error traceback to the appropriate file.

    Parameters:
        traceback: the error traceback to log
    """
    logger = _get_logger("error_traceback.log")
    logger.error(f"{str(datetime.now())} | {traceback}")
