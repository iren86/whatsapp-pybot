# -*- coding: utf-8 -*-
import json
import os
import sys

project_dir = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
# add the project directory to sys.path
sys.path.append(project_dir)
#

from pybot.whatsapp.util import FileUtil
from pybot.whatsapp.core import CmdParser
from pybot.whatsapp.driver.ChromeFactory import ChromeFactory
from pybot.whatsapp.feature.AppPageFeature import AppPageFeature
from pybot.whatsapp.feature.WelcomePageFeature import WelcomePageFeature
from pybot.whatsapp.core.LoggerFactory import get_logger

logger = get_logger()


def validate_file_path(file_path):
    if not file_path:
        CmdParser.print_help()
        raise ValueError("No file provided")

    if not os.path.isfile(file_path):
        CmdParser.print_help()
        raise ValueError("File %s not exists" % file_path)

    return file_path


def process_input(users, message):
    assert isinstance(users, list), "users must be a list"
    assert message, "message must be provided"

    processed_users = []
    skipped_users = []

    driver = None
    try:
        driver = ChromeFactory.create_chrome()

        welcome_page = WelcomePageFeature(driver)
        app_page = AppPageFeature(driver)

        welcome_page.open_welcome_page()
        welcome_page.wait_for_phone_scan_complete()

        app_page.is_app_page()

        logger.info("Start sending message to %s user(s)" % len(users))
        for user in users:
            if app_page.open_chat_with_user(user):
                # send message only if chat opened with the user
                logger.info("Send next message to the user '%s'\n%s\n" % (user, message))
                app_page.send_message(message)
                logger.info("Ok. Message sent to the user '%s'" % user)
                processed_users.append(user)
            else:
                logger.warning("User '%s' not found in contact list" % user)
                skipped_users.append(user)
                app_page.close_search_drawer()

        logger.info(
            "Logout from the app. Users processed: %s, skipped: %s" % (len(processed_users), len(skipped_users)))
        app_page.logout()
        logger.info("Logout completed")

    finally:
        logger.info("Processed users:\n%s" % json.dumps(processed_users))
        logger.info("Skipped users:\n%s" % json.dumps(skipped_users))

        if driver:
            driver.quit()


def run_app():
    # print help if --help/-h argument provided
    CmdParser.check_if_help()

    users_file_path = validate_file_path(CmdParser.get_users_file_path())
    message_file_path = validate_file_path(CmdParser.get_message_file_path())

    users = FileUtil.read_file_lines(users_file_path)
    message = FileUtil.read_file(message_file_path)

    process_input(users, message)


if __name__ == "__main__":
    #
    # To start application run the next command within the project directory:
    # ./venv/bin/python2.7 ./pybot/whatsapp/Bot.py -u ./resources/users_sample.txt -m ./resources/message_sample.txt
    #
    run_app()
