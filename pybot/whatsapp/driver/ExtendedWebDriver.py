# -*- coding: utf-8 -*-

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener

from pybot.whatsapp.core.LoggerFactory import get_logger

NUMBER_OF_RETRIES = 3


def _wrap_elements(result, ef_driver):
    if isinstance(result, WebElement):
        return ExtendedWebElement(result, ef_driver)
    elif isinstance(result, list):
        return [_wrap_elements(item, ef_driver) for item in result]
    else:
        return result


class ExtendedWebDriver(object):
    """
    A wrapper around an arbitrary WebDriver instance which supports firing events
    """

    def __init__(self, driver, event_listener):
        """
        Creates a new instance of the ExtendedWebDriver

        :Args:
         - driver : A WebDriver instance
         - event_listener : Instance of a class that subclasses AbstractEventListener and implements it fully or partially

        Example:

        .. code-block:: python

            from selenium.webdriver import Firefox
            from selenium.webdriver.support.events import ExtendedWebDriver, AbstractEventListener

            class MyListener(AbstractEventListener):
                def before_navigate_to(self, url, driver):
                    print("Before navigate to %s" % url)
                def after_navigate_to(self, url, driver):
                    print("After navigate to %s" % url)

            driver = Firefox()
            ef_driver = ExtendedWebDriver(driver, MyListener())
            ef_driver.get("http://www.google.co.in/")
        """
        if not isinstance(driver, WebDriver):
            raise WebDriverException("A WebDriver instance must be supplied")
        if not isinstance(event_listener, AbstractEventListener):
            raise WebDriverException("Event listener must be a subclass of AbstractEventListener")
        self._driver = driver
        self._driver._wrap_value = self._wrap_value
        self._listener = event_listener

    @property
    def wrapped_driver(self):
        """Returns the WebDriver instance wrapped by this EventsFiringWebDriver"""
        return self._driver

    def get(self, url):
        count = 1
        while count <= NUMBER_OF_RETRIES:  # try n times
            try:
                self._dispatch("navigate_to", (url, self._driver), "get", (url,))
                break
            except Exception as e:
                # If trying n time and still error?
                if count == NUMBER_OF_RETRIES:
                    get_logger().error(
                        "Get url method failed after number of retries: %s, "
                        "with exception:" % str(count), e
                    )
                    raise
                count += 1

    def back(self):
        self._dispatch("navigate_back", (self._driver,), "back", ())

    def forward(self):
        self._dispatch("navigate_forward", (self._driver,), "forward", ())

    def execute_script(self, script, *args):
        unwrapped_args = (script,) + self._unwrap_element_args(args)
        return self._dispatch("execute_script", (script, self._driver), "execute_script", unwrapped_args)

    def execute_async_script(self, script, *args):
        unwrapped_args = (script,) + self._unwrap_element_args(args)
        return self._dispatch("execute_script", (script, self._driver), "execute_async_script", unwrapped_args)

    def close(self):
        self._dispatch("close", (self._driver,), "close", ())

    def quit(self):
        self._dispatch("quit", (self._driver,), "quit", ())

    def find_element(self, by=By.ID, value=None):
        return self._dispatch("find", (by, value, self._driver), "find_element", (by, value))

    def find_elements(self, by=By.ID, value=None):
        return self._dispatch("find", (by, value, self._driver), "find_elements", (by, value))

    def find_element_by_id(self, id_):
        return self.find_element(by=By.ID, value=id_)

    def find_elements_by_id(self, id_):
        return self.find_elements(by=By.ID, value=id_)

    def find_element_by_xpath(self, xpath):
        return self.find_element(by=By.XPATH, value=xpath)

    def find_elements_by_xpath(self, xpath):
        return self.find_elements(by=By.XPATH, value=xpath)

    def find_element_by_link_text(self, link_text):
        return self.find_element(by=By.LINK_TEXT, value=link_text)

    def find_elements_by_link_text(self, text):
        return self.find_elements(by=By.LINK_TEXT, value=text)

    def find_element_by_partial_link_text(self, link_text):
        return self.find_element(by=By.PARTIAL_LINK_TEXT, value=link_text)

    def find_elements_by_partial_link_text(self, link_text):
        return self.find_elements(by=By.PARTIAL_LINK_TEXT, value=link_text)

    def find_element_by_name(self, name):
        return self.find_element(by=By.NAME, value=name)

    def find_elements_by_name(self, name):
        return self.find_elements(by=By.NAME, value=name)

    def find_element_by_tag_name(self, name):
        return self.find_element(by=By.TAG_NAME, value=name)

    def find_elements_by_tag_name(self, name):
        return self.find_elements(by=By.TAG_NAME, value=name)

    def find_element_by_class_name(self, name):
        return self.find_element(by=By.CLASS_NAME, value=name)

    def find_elements_by_class_name(self, name):
        return self.find_elements(by=By.CLASS_NAME, value=name)

    def find_element_by_css_selector(self, css_selector):
        return self.find_element(by=By.CSS_SELECTOR, value=css_selector)

    def find_elements_by_css_selector(self, css_selector):
        return self.find_elements(by=By.CSS_SELECTOR, value=css_selector)

    def make_screenshot(self, file_path):
        assert file_path is not None, "File path must be initialized"

        try:
            url = self._driver.current_url
            log_message = "%s %s" % (url, file_path)

            get_logger().error(log_message)
            self._driver.save_screenshot(file_path)
        except Exception as e:
            url = self._driver.current_url
            get_logger().error(
                "Can't make a screenshot. "
                "Probably because alert window in focus: %s. "
                "Type error: %s. "
                "Url: %s" % (e, type(e).__name__, url))

    def save_page_source(self, file_path):
        assert file_path is not None, "File path must be initialized"

        try:
            url = self._driver.current_url

            log_message = "%s %s" % (url, file_path)

            get_logger().error(log_message)
            html = self._driver.page_source
            with open(file_path, "w") as f:
                f.write(html.encode("utf-8"))
        except Exception as e:
            url = self._driver.current_url
            get_logger().error(
                "Can't save page source. "
                "Probably because alert window in focus: %s. "
                "Type error: %s. "
                "Url: %s" % (e, type(e).__name__, url))

    def _dispatch(self, l_call, l_args, d_call, d_args):
        getattr(self._listener, "before_%s" % l_call)(*l_args)
        try:
            result = getattr(self._driver, d_call)(*d_args)
        except Exception as e:
            self._listener.on_exception(e, self)
            raise e
        getattr(self._listener, "after_%s" % l_call)(*l_args)
        return _wrap_elements(result, self)

    def _unwrap_element_args(self, args):
        if isinstance(args, ExtendedWebElement):
            return args.wrapped_element
        elif isinstance(args, tuple):
            return tuple([self._unwrap_element_args(item) for item in args])
        elif isinstance(args, list):
            return [self._unwrap_element_args(item) for item in args]
        else:
            return args

    def _wrap_value(self, value):
        if isinstance(value, ExtendedWebElement):
            return WebDriver._wrap_value(self._driver, value.wrapped_element)
        return WebDriver._wrap_value(self._driver, value)

    def __setattr__(self, item, value):
        if item.startswith("_") or not hasattr(self._driver, item):
            object.__setattr__(self, item, value)
        else:
            try:
                object.__setattr__(self._driver, item, value)
            except Exception as e:
                self._listener.on_exception(e, self)
                raise e

    def __getattr__(self, name):

        def _wrap(*args):
            try:
                result = attrib(*args)
                return _wrap_elements(result, self)
            except Exception as e:
                self._listener.on_exception(e, self)
                raise e

        if hasattr(self._driver, name):
            try:
                attrib = getattr(self._driver, name)
                if not callable(attrib):
                    return attrib
            except Exception as e:
                self._listener.on_exception(e, self)
                raise e
            return _wrap

        raise AttributeError(name)


class ExtendedWebElement(object):
    """"
    A wrapper around WebElement instance which supports firing events
    """

    def __init__(self, webelement, ef_driver):
        """
        Creates a new instance of the ExtendedWebElement
        """
        self._webelement = webelement
        self._ef_driver = ef_driver
        self._driver = ef_driver.wrapped_driver
        self._listener = ef_driver._listener

    @property
    def wrapped_element(self):
        """Returns the WebElement wrapped by this ExtendedWebElement instance"""
        return self._webelement

    def click(self):
        self._dispatch("click", (self._webelement, self._driver), "click", ())

    def clear(self):
        self._dispatch("change_value_of", (self._webelement, self._driver), "clear", ())

    def send_keys(self, *value):
        self._dispatch("change_value_of", (self._webelement, self._driver), "send_keys", value)

    def find_element(self, by=By.ID, value=None):
        return self._dispatch("find", (by, value, self._driver), "find_element", (by, value))

    def find_elements(self, by=By.ID, value=None):
        return self._dispatch("find", (by, value, self._driver), "find_elements", (by, value))

    def find_element_by_id(self, id_):
        return self.find_element(by=By.ID, value=id_)

    def find_elements_by_id(self, id_):
        return self.find_elements(by=By.ID, value=id_)

    def find_element_by_name(self, name):
        return self.find_element(by=By.NAME, value=name)

    def find_elements_by_name(self, name):
        return self.find_elements(by=By.NAME, value=name)

    def find_element_by_link_text(self, link_text):
        return self.find_element(by=By.LINK_TEXT, value=link_text)

    def find_elements_by_link_text(self, link_text):
        return self.find_elements(by=By.LINK_TEXT, value=link_text)

    def find_element_by_partial_link_text(self, link_text):
        return self.find_element(by=By.PARTIAL_LINK_TEXT, value=link_text)

    def find_elements_by_partial_link_text(self, link_text):
        return self.find_elements(by=By.PARTIAL_LINK_TEXT, value=link_text)

    def find_element_by_tag_name(self, name):
        return self.find_element(by=By.TAG_NAME, value=name)

    def find_elements_by_tag_name(self, name):
        return self.find_elements(by=By.TAG_NAME, value=name)

    def find_element_by_xpath(self, xpath):
        return self.find_element(by=By.XPATH, value=xpath)

    def find_elements_by_xpath(self, xpath):
        return self.find_elements(by=By.XPATH, value=xpath)

    def find_element_by_class_name(self, name):
        return self.find_element(by=By.CLASS_NAME, value=name)

    def find_elements_by_class_name(self, name):
        return self.find_elements(by=By.CLASS_NAME, value=name)

    def find_element_by_css_selector(self, css_selector):
        return self.find_element(by=By.CSS_SELECTOR, value=css_selector)

    def find_elements_by_css_selector(self, css_selector):
        return self.find_elements(by=By.CSS_SELECTOR, value=css_selector)

    def _dispatch(self, l_call, l_args, d_call, d_args):
        getattr(self._listener, "before_%s" % l_call)(*l_args)
        try:
            result = getattr(self._webelement, d_call)(*d_args)
        except Exception as e:
            self._listener.on_exception(e, self)
            raise e
        getattr(self._listener, "after_%s" % l_call)(*l_args)
        return _wrap_elements(result, self._ef_driver)

    def __setattr__(self, item, value):
        if item.startswith("_") or not hasattr(self._webelement, item):
            object.__setattr__(self, item, value)
        else:
            try:
                object.__setattr__(self._webelement, item, value)
            except Exception as e:
                self._listener.on_exception(e, self)
                raise e

    def __getattr__(self, name):

        def _wrap(*args):
            try:
                result = attrib(*args)
                return _wrap_elements(result, self._ef_driver)
            except Exception as e:
                self._listener.on_exception(e, self)
                raise e

        if hasattr(self._webelement, name):
            try:
                attrib = getattr(self._webelement, name)
                if not callable(attrib):
                    return attrib
            except Exception as e:
                self._listener.on_exception(e, self)
                raise e
            return _wrap

        raise AttributeError(name)
