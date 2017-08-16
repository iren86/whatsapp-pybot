# -*- coding: utf-8 -*-
from functools import partial

from selenium.webdriver.common.by import By

from pybot.whatsapp.feature.BaseFeature import BaseFeature
from pybot.whatsapp.util import WaitUtil

WAIT_FOR_QR_CODE_TIMEOUT_IN_SEC = 600


class WelcomePageFeature(BaseFeature):
    SCAN_IMAGE = (
        By.XPATH,
        '//img[contains(@alt, "Scan me")]'
    )

    def open_welcome_page(self):
        self.driver.get("https://web.whatsapp.com/")

    def wait_for_phone_scan_complete(self):
        WaitUtil.wait_for_result_is_false(partial(self.is_element_exists, WelcomePageFeature.SCAN_IMAGE),
                                          WAIT_FOR_QR_CODE_TIMEOUT_IN_SEC,
                                          "!!! Scan the QR code that appears on the Chrome browser screen with WhatsApp app on your phone. Waiting ....")
        self.random_sleep_between_requests()
