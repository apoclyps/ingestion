#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
parser
----------------------------------
Handles parsing and sanitisation of records to item models
"""

from ingestion import validate
from ingestion import models

# defines sanitisation required for csv record input
ITEM_SANITISATION = {
    'id': validate.is_valid_int,
    'description': validate.is_valid_description,
    'price': validate.is_valid_float,
    'cost': validate.is_valid_float,
    'quantity_on_hand': validate.is_valid_int,
    'price_type': validate.is_valid_price_type
}


def parse_inventory_item(record):
    """ Converts a csv inventory item record to a inventory item model """
    if not isinstance(record, dict):
        raise Exception

    item = models.InventoryItem()
    modifier_map = {}

    for key in record:
        # handles parsing of item id field name to id
        if key == 'item id':
            record['id'] = record[key]
            del record[key]
            key = 'id'

        # handles removal of currency symbol from value
        value = str(record[key]).replace('$', '')

        if value is None:
            continue

        # set model property for non-modifier keys; modifier keys state stored in modifier_map
        if key in ITEM_SANITISATION:
            value = ITEM_SANITISATION[key](value)
            setattr(item, validate.enforce_key_consistency(key), value)
        elif 'modifier_' in key:
            modifier_map = __create_update_price_modifiers(key, record[key], modifier_map)
        else:
            setattr(item, validate.enforce_key_consistency(key), record[key])

    # updates modifiers when all keys have been parsed
    modifiers = [modifier_map[key] for key in modifier_map]
    setattr(item, validate.enforce_key_consistency('modifiers'), modifiers)

    return item


def __create_update_price_modifiers(key, value, modifier_map):
    """ Handles creation and updating of price modifier map """
    (_, identifier, field_name) = validate.regex_match_modifiers(key)

    modifier = modifier_map.get(identifier, dict())

    if value is not None and not value.isalpha():
        value = value.replace('$', '')
        value = validate.is_valid_float(value)

    if value is not None:
        modifier[field_name] = value
        modifier_map[identifier] = modifier

    return modifier_map
