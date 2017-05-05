# -*- coding: utf-8 -*-
import inspect
import os
from datetime import datetime

from pybot.whatsapp.util import FileUtil

TESTS_PACKAGE_PATH = "pybot/whatsapp/feature/"


def find_test_caller_in_stack():
    # skip all Base* files
    result = [caller for caller in inspect.stack() if
              TESTS_PACKAGE_PATH in caller[1] and not caller[1].split(os.sep)[-1].startswith('Base')]
    if result:
        # return (class, method)
        return (result[0][1], result[0][3])
    raise ValueError("Caller from test package not found! Method call must be initiated from test class.")


def get_file_name():
    datetimenow = datetime.now()
    datestr = datetimenow.strftime("%Y-%m-%d")
    timestr = datetimenow.strftime("%H-%M-%S")

    file_name = None

    try:
        test_class_path, test_method_name = find_test_caller_in_stack()
        test_package_path, test_file_name = os.path.split(test_class_path)

        # identify main package name from the class
        # for example: pybot/whatsapp/feature/AppPageFeature.py -> feature
        test_package_name = test_package_path.split(os.sep)[-1:][0]
        test_class_name = test_file_name.split(os.extsep)[0]

        file_name = "%s-%s-%s-%s" % (
            test_package_name, test_class_name, datestr, timestr
        )
    except ValueError:
        file_name = "%s-%s" % (datestr, timestr)

    return file_name


def new_screenshot_path():
    file_name = "%s.png" % get_file_name()

    file_path = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     os.pardir, os.pardir, os.pardir,
                     "screenshots", file_name))
    FileUtil.mkdirs(file_path)

    return file_path


def new_pagesource_path():
    file_name = "%s.html" % get_file_name()

    file_path = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     os.pardir, os.pardir, os.pardir,
                     "pagesource", file_name))
    FileUtil.mkdirs(file_path)

    return file_path
