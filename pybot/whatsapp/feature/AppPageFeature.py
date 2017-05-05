# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pybot.whatsapp.feature.BaseFeature import BaseFeature


class AppPageFeature(BaseFeature):
    CHAT_ICON = (
        By.XPATH,
        "//button[contains(@class, 'icon-chat')]"
    )
    INPUT_SEARCH_FIELD = (
        By.XPATH,
        "//input[contains(@class, 'input-search')]"
    )
    USER_IN_SEARCH_LIST = (
        By.XPATH,
        "//span[contains(@title, '%s')]"
    )
    INPUT_MESSAGE_FIELD = (
        By.XPATH,
        '//div[@class="input"][@dir="auto"][@data-tab="1"]'
    )
    MENU_ICON = (
        By.XPATH,
        "//button[contains(@class, 'icon-menu')]"
    )
    LOGOUT_MENU_ITEM = (
        By.XPATH,
        "//div[contains(@title, 'Log out')]"
    )

    def is_app_page(self):
        WebDriverWait(self.driver, self.get_request_timeout_in_sec()).until(
            EC.presence_of_element_located(self.CHAT_ICON))
        self.random_sleep_between_requests()

    def open_chat_with_user(self, username):
        assert username, "User name must be provided"

        icon_chat = WebDriverWait(self.driver, self.get_request_timeout_in_sec()).until(
            EC.presence_of_element_located(self.CHAT_ICON))
        icon_chat.click()
        self.random_sleep_between_requests()

        input_search_field = WebDriverWait(self.driver, self.get_request_timeout_in_sec()).until(
            EC.presence_of_element_located(self.INPUT_SEARCH_FIELD))
        input_search_field.clear()
        self.random_sleep_send_keys(input_search_field, username)
        self.random_sleep_between_requests()

        user_in_list = WebDriverWait(self.driver, self.get_request_timeout_in_sec()).until(
            EC.presence_of_element_located(self.build_user_in_search_list_locator_for_user(username)))
        user_in_list.click()
        self.random_sleep_between_requests()

    def send_message(self, msg):
        assert msg, "Message must be provided"

        input_message_field = WebDriverWait(self.driver, self.get_request_timeout_in_sec()).until(
            EC.presence_of_element_located(self.INPUT_MESSAGE_FIELD))
        input_message_field.clear()
        self.random_sleep_send_keys(input_message_field, msg + Keys.ENTER)
        self.random_sleep_between_requests()

    def logout(self):
        menu_icon = WebDriverWait(self.driver, self.get_request_timeout_in_sec()).until(
            EC.presence_of_element_located(self.MENU_ICON))
        menu_icon.click()
        self.random_sleep_between_requests()

        logout_menu_item = WebDriverWait(self.driver, self.get_request_timeout_in_sec()).until(
            EC.presence_of_element_located(self.LOGOUT_MENU_ITEM))
        logout_menu_item.click()
        self.random_sleep_between_requests()

    def build_user_in_search_list_locator_for_user(self, username):
        return (
            AppPageFeature.USER_IN_SEARCH_LIST[0],
            AppPageFeature.USER_IN_SEARCH_LIST[1] % username
        )
