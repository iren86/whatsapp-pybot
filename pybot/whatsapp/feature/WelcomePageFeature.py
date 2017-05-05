# -*- coding: utf-8 -*-
from functools import partial

from selenium.webdriver.common.by import By

from pybot.whatsapp.feature.BaseFeature import BaseFeature
from pybot.whatsapp.util import WaitUtil


class WelcomePageFeature(BaseFeature):
    SCAN_IMAGE = (
        By.XPATH,
        '//img[contains(@alt, "Scan me")]'
    )

    def open_welcome_page(self):
        self.driver.get("https://web.whatsapp.com/")

    def wait_for_phone_scan_complete(self):
        WaitUtil.wait_for_result_is_false(partial(self.is_element_exists, WelcomePageFeature.SCAN_IMAGE),
                                          self.get_request_timeout_in_sec(),
                                          "!!! Please Scan the QR code that appears on the Chrome browser screen with WhatsApp app on your phone. Waiting ....")
        self.random_sleep_between_requests()
