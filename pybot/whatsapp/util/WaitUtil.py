# -*- coding: utf-8 -*-
import time

from pybot.whatsapp.core.LoggerFactory import get_logger

POLL_FREQUENCY = 0.5
# message will be posted every POLL_FREQUENCY * POST_WAIT_MSG_EVERY_ITERATION second
POST_WAIT_MSG_EVERY_ITERATION = 10

logger = get_logger()


def wait_for_result(method, timeout, wait_msg=None):
    """Calls the method until the return value is True."""

    count = 0
    result = None
    end_time = time.time() + timeout
    while True:
        try:
            result = method()
            if result:
                return result
        except:
            pass

        time.sleep(POLL_FREQUENCY)
        if time.time() > end_time:
            break

        if wait_msg and count % POST_WAIT_MSG_EVERY_ITERATION == 0:
            get_logger().warning(wait_msg)

        count += 1

    return result


def wait_for_result_is_none(method, timeout, wait_msg=None):
    """Calls the method until the return value is None."""

    count = 0
    end_time = time.time() + timeout
    while True:
        try:
            result = method()
            if result is None:
                return True
        except:
            pass

        time.sleep(POLL_FREQUENCY)
        if time.time() > end_time:
            break

        if wait_msg and count % POST_WAIT_MSG_EVERY_ITERATION == 0:
            get_logger().warning(wait_msg)

        count += 1

    return False


def wait_for_result_is_false(method, timeout, wait_msg=None):
    """Calls the method until the return value is False."""

    count = 0
    end_time = time.time() + timeout
    while True:
        try:
            result = method()
            if not result:
                return True
        except:
            pass

        time.sleep(POLL_FREQUENCY)
        if time.time() > end_time:
            break

        if wait_msg and count % POST_WAIT_MSG_EVERY_ITERATION == 0:
            get_logger().warning(wait_msg)

        count += 1

    return False
