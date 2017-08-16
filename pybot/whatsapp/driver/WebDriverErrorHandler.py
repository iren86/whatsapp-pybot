# -*- coding: utf-8 -*-

from selenium.webdriver.support.events import AbstractEventListener

from pybot.whatsapp.core.LoggerFactory import get_logger
from pybot.whatsapp.util.AppUtil import new_pagesource_path
from pybot.whatsapp.util.AppUtil import new_screenshot_path


class WebDriverErrorHandler(AbstractEventListener):
    logger = get_logger()

    def on_exception(self, exception, driver):
        screenshot_path = new_screenshot_path()
        pagesource_path = new_pagesource_path()

        try:
            url = driver.current_url
            # status_code = self.get_status_code(url)
            # error_message = "HTTP/%s %s %s:\n%s" % (status_code, url, file_path, str(exception))

            error_message = "%s %s:\n%s" % (url, screenshot_path, str(exception))

            self.logger.exception(error_message)
            driver.make_screenshot(screenshot_path)
            driver.save_page_source(pagesource_path)
        except Exception as e:
            self.logger.error(
                "Can't make a screenshot or can't get a page source. "
                "Probably because alert window in focus: %s" % str(e)
            )
