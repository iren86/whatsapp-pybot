# -*- coding: utf-8 -*-

from random import uniform
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from pybot.whatsapp.driver import ChromeFactory
from pybot.whatsapp.util.AppUtil import new_pagesource_path
from pybot.whatsapp.util.AppUtil import new_screenshot_path

RANDOM_SLEEP_BETWEEN_REQUESTS_START = 0.5
RANDOM_SLEEP_BETWEEN_REQUESTS_END = 2.0

RANDOM_SLEEP_BETWEEN_SEND_KEYS_START = 0.05
RANDOM_SLEEP_BETWEEN_SEND_KEYS_END = 0.15


class BaseFeature(object):
    """Base class to initialize the base feature that will be called from all features"""

    def __init__(self, driver):

        self.driver = driver

    def disable_leave_page_popup(self):
        '''
        Disable popup saying "Are you sure?
        The page is asking you to confirm that you want to leave - data entered will be lost."
        with 2 buttons: Leave Page and Stay on Page
        :return:
        '''
        # firefox version
        self.driver.execute_script("window.onbeforeunload = function(e){};")
        # chrome version
        self.driver.execute_script('$(window).unbind("beforeunload");')

    def is_valid(self, validator, message, *args):

        screenshot_path = new_screenshot_path()
        pagesource_path = new_pagesource_path()

        try:
            if args is not None:
                assert validator(*args), message
            else:
                assert validator(), message
        except Exception:
            self.driver.make_screenshot(screenshot_path)
            self.driver.save_page_source(pagesource_path)
            raise

    def is_element_exists(self, locator):
        assert len(locator) == 2, "Locator must consists from By expression (0) and element locator (1)"

        try:
            self.driver.find_element(locator[0], locator[1])
        except NoSuchElementException:
            # driver.find_element raise only NoSuchElementException
            return False
        return True

    def random_sleep_between_requests(self):
        '''
        Random delays between the requests to avoid getting blocked
        '''
        sleep(uniform(RANDOM_SLEEP_BETWEEN_REQUESTS_START, RANDOM_SLEEP_BETWEEN_REQUESTS_END))

    def random_sleep_send_keys(self, field, text):
        '''
        Type letter by letter to avoid getting blocked
        '''
        assert field, "Field must be provided"
        assert text, "Text must be provided"

        for letter in text:
            field.send_keys(letter)
            sleep(uniform(RANDOM_SLEEP_BETWEEN_SEND_KEYS_START, RANDOM_SLEEP_BETWEEN_SEND_KEYS_END))

    def get_request_timeout_in_sec(self):

        return ChromeFactory.REQUEST_TIMEOUT_IN_SEC
