#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
models
----------------------------------
Models store record state during parsing and serialisation to other formats.
"""


class InventoryItem(object):
    """ Inventory Item Model """

    def __init__(self, id=None, price=None, description=None, cost=None, price_type=None,
                 quantity_on_hand=None, modifiers=[]):
        self._id = id
        self._price = price
        self._description = description
        self._cost = cost
        self._price_type = price_type
        self._quantity_on_hand = quantity_on_hand
        self._modifiers = modifiers

    @property
    def id(self):
        """ get id property """
        return self._id

    @id.setter
    def id(self, id):
        """ set id property """
        self._id = id

    @property
    def price(self):
        """ get price property """
        return self._price

    @price.setter
    def price(self, price):
        """ set price property """
        self._price = price

    @property
    def description(self):
        """ get description property """
        return self._description

    @description.setter
    def description(self, _description):
        """ set description property """
        self._description = _description

    @property
    def cost(self):
        """ set cost property """
        return self._cost

    @cost.setter
    def cost(self, cost):
        """ get cost property """
        self._cost = cost

    @property
    def price_type(self):
        """ get price_type property """
        return self._price_type

    @price_type.setter
    def price_type(self, price_type):
        """ set price_type property """
        self._price_type = price_type

    @property
    def quantity_on_hand(self):
        """ set quantity_on_hand property """
        return self._quantity_on_hand

    @quantity_on_hand.setter
    def quantity_on_hand(self, quantity_on_hand):
        """ get quantity_on_hand property """
        self._quantity_on_hand = quantity_on_hand

    @property
    def modifiers(self):
        """ get modifiers property """
        return self._modifiers

    @modifiers.setter
    def modifiers(self, modifiers):
        """ set modifiers property """
        self._modifiers = modifiers
