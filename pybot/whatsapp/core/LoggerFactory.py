# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime

from pybot.whatsapp.util import FileUtil
from pybot.whatsapp.util.ThreadlocalUtil import get_threadlocal_var, set_threadlocal_var

ROOT_LOGGER_VAR = "root_logger"
ROOT_LOGGER_FILE_NAME_VAR = "root_logger_file_name"


def get_logger():
    """Function to build preconfigured logger instance"""

    root_logger = get_threadlocal_var(ROOT_LOGGER_VAR)

    if root_logger is None:
        log_file_name = get_logger_file_name()

        root_logger = set_threadlocal_var(ROOT_LOGGER_VAR, logging.getLogger(log_file_name))
        root_logger.setLevel(logging.INFO)

        log_file_path = os.path.normpath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         os.pardir, os.pardir, os.pardir, "reports", log_file_name))
        FileUtil.mkdirs(log_file_path)
        fileHandler = logging.FileHandler(log_file_path, "w")
        fileHandler.setLevel(logging.WARN)
        fileHandler.setFormatter(
            logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"))
        root_logger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logging.Formatter("%(message)s"))
        root_logger.addHandler(consoleHandler)

    return root_logger


def get_logger_file_name():
    file_name = get_threadlocal_var(ROOT_LOGGER_FILE_NAME_VAR)
    if file_name:
        return file_name

    datetimenow = datetime.now()
    datetimestr = datetimenow.strftime("%Y_%m_%d_%H_%M_%S")

    return set_threadlocal_var(ROOT_LOGGER_FILE_NAME_VAR, "whatsapp_pybot_%s.log" % datetimestr)
