#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
validate
----------------------------------
provides helper functions for sanitizing data when parsing
"""

import re
from string import digits

# captures modifiers in the following groups: (word)(_)(int)(_)(word)
MODIFIER_REGEX = '((?:[a-z][a-z]+))(_)(\\d+)(_)((?:[a-z][a-z]+))'

PRICE_TYPE_OPEN = 'open'
PRICE_TYPE_SYSTEM = 'system'


def is_valid_int(value):
    """ Returns value if valid cast to integer, otherwise none """
    try:
        value = int(value)
    except ValueError:
        value = None

    return value


def is_valid_float(value):
    """ Returns value if valid cast to float, otherwise none """
    try:
        value = float(value)
    except ValueError:
        value = None

    return value


def is_valid_string(value):
    """ Returns value if valid cast to string, otherwise none """
    try:
        value = str(value)
    except ValueError:
        value = None

    return value


def is_valid_description(value):
    """ Returns alpha string """
    remove_digits = str.maketrans('', '', digits)
    value = value.translate(remove_digits)

    if len(value) > 0 and value[-1:] == ' ':
        value = value[:-1]

    return value


def is_valid_price_type(value):
    """ Returns value if valid maps to supported price types, otherwise an Exception is raised """
    value = value.lower().replace(' ', '')
    if value == PRICE_TYPE_OPEN or value == PRICE_TYPE_SYSTEM:
        return value
    else:
        raise Exception('Unsupported price type')


def enforce_key_consistency(key):
    """ Forces all keys to lowercase and replaces spaces with underscores """
    return str(key.replace(' ', '_').lower())


def regex_match_modifiers(txt):
    """ Returns regex capture group if text is valid, otherwise none """
    regex = re.compile(MODIFIER_REGEX, re.IGNORECASE | re.DOTALL)
    match = regex.search(txt)

    if match is not None:
        modifier = match.group(1)
        mod_identifier = match.group(3)
        modifier_field = match.group(5)
        return modifier, mod_identifier, modifier_field

    return None
