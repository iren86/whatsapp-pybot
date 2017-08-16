# -*- coding: utf-8 -*-
import os.path
from sys import platform

from selenium import webdriver

from pybot.whatsapp.driver.ExtendedWebDriver import ExtendedWebDriver
from pybot.whatsapp.driver.WebDriverErrorHandler import WebDriverErrorHandler

# Request default configuration
PAGE_LOAD_TIMEOUT_IN_SEC = 5
IMPLICITLY_WAIT_IN_SEC = 5
SCRIPT_TIMEOUT_IN_SEC = 5
REQUEST_TIMEOUT_IN_SEC = 10


class ChromeFactory:
    @staticmethod
    def create_chrome():
        """
        Build default Chrome instance.
        """
        chrome_driver_path = ChromeFactory.get_driver_path()
        chrome_options = ChromeFactory.build_chrome_options()

        driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=chrome_options)

        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT_IN_SEC)
        driver.implicitly_wait(IMPLICITLY_WAIT_IN_SEC)
        driver.set_script_timeout(SCRIPT_TIMEOUT_IN_SEC)

        driver_wrapper = ExtendedWebDriver(driver, WebDriverErrorHandler())
        return driver_wrapper

    @staticmethod
    def build_chrome_options():

        chrome_options = webdriver.ChromeOptions()
        chrome_options.accept_untrusted_certs = True
        chrome_options.assume_untrusted_cert_issuer = True
        # chrome configuration
        # More: https://github.com/SeleniumHQ/docker-selenium/issues/89
        # And: https://github.com/SeleniumHQ/docker-selenium/issues/87
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-impl-side-painting")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--disable-seccomp-filter-sandbox")
        chrome_options.add_argument("--disable-breakpad")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-cast")
        chrome_options.add_argument("--disable-cast-streaming-hw-encoding")
        chrome_options.add_argument("--disable-cloud-import")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-session-crashed-bubble")
        chrome_options.add_argument("--disable-ipv6")
        chrome_options.add_argument("--allow-http-screen-capture")
        chrome_options.add_argument("--start-maximized")

        return chrome_options

    @staticmethod
    def get_driver_path():

        chrome_driver_folder_name = ""
        if platform == "linux" or platform == "linux2":
            # linux
            chrome_driver_folder_name = "linux_x64"
        elif platform == "darwin":
            # OS X
            chrome_driver_folder_name = "mac_x64"
        else:
            raise ValueError("Platform not identified")

        chrome_driver_path = os.path.normpath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         os.pardir, os.pardir, os.pardir,
                         "resources", "chrome", chrome_driver_folder_name,
                         "chromedriver"))
        assert os.path.isfile(chrome_driver_path), \
            "Chrome driver must exists: %s" % chrome_driver_path

        return chrome_driver_path
