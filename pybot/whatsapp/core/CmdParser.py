# -*- coding: utf-8 -*-
import optparse

parser = None


def get_option_parser():
    global parser
    if parser is None:
        parser = optparse.OptionParser()
        parser.add_option('-u', action="store", help="Select file with users")
        parser.add_option('-m', action="store", help="Select file with message")
    return parser


def print_help():
    parser.print_help()


def check_if_help():
    parser = get_option_parser()
    parser.parse_args()


def get_users_file_path():
    parser = get_option_parser()
    options, args = parser.parse_args()
    return options.u


def get_message_file_path():
    parser = get_option_parser()
    options, args = parser.parse_args()
    return options.m
