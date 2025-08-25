import logging
import os
from src.common.constants import APP_NAME
from src.common.constants import DEFAULT_LOG_LEVEL
from src.common.constants import LOGS_PATH
from src.common.utils import generate_timestamp_pattern


IS_ROOT_LOGGER_CONFIGURED = False


def get_logger(logger_name: str = APP_NAME, logger_caller: str = None, level: str = DEFAULT_LOG_LEVEL, logger_filename = APP_NAME, flag_stdout: bool = False) -> logging.Logger:
    global IS_ROOT_LOGGER_CONFIGURED
    if not IS_ROOT_LOGGER_CONFIGURED:
        logging.basicConfig(handlers=[logging.NullHandler()])  # Set up the default root logger to do nothing 
        IS_ROOT_LOGGER_CONFIGURED = True
    if logger_name == '__main__' and logger_caller != None:
        logger = logging.getLogger(logger_caller)  # Creates a named logger using logger_caller.
    else:
        logger = logging.getLogger(logger_name)  # Creates a named logger.
    if level in logging._nameToLevel:
        LEVEL = logging._nameToLevel.get(level)
    else:
        LEVEL = logging._nameToLevel.get(DEFAULT_LOG_LEVEL)
    logger.setLevel(LEVEL)
    filename = os.path.basename(logger_filename)
    filename_base = filename
    if filename.endswith(".py"):
        filename_base = filename[:-3]
    _logger_filename = generate_timestamp_pattern(
        basename=filename_base,
        timestamp_format="%Y_%m_%d",
        extension="log"
    )
    if os.path.isdir(LOGS_PATH):
        logger_full_filename = os.path.join(LOGS_PATH, _logger_filename)
        file_handler = logging.FileHandler(
            filename=logger_full_filename,
            mode='a+'
        )
        file_handler_formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %I:%M:%S %p"
        )
        file_handler.setFormatter(fmt=file_handler_formatter)
        logger.addHandler(hdlr=file_handler)
    else:
        flag_stdout = True
    if flag_stdout:
        console_handler = logging.StreamHandler()
        console_handler_formater = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %I:%M:%S %p"
        )
        console_handler.setFormatter(fmt=console_handler_formater)
        console_handler.setLevel(level=logging.INFO)
        logger.addHandler(hdlr=console_handler)
    return logger