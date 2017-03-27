#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_validation
----------------------------------
Tests for `ingestion` module.
"""
import operator
import unittest
import json

from ingestion import file_io, parser, models, validate
from ingestion.conversion_factory import ConversionFactory, CSVConversion, XMLConversion


class TestConversionFactory(unittest.TestCase):
    def test_should_fail_if_not_csv_conversion_factory(self):
        factory = ConversionFactory.create_conversion('CSVConversion')
        self.assertIsInstance(factory, CSVConversion)

    def test_should_fail_if_multiple_factories_not_created(self):
        ConversionFactory.create_conversion('XMLConversion')
        ConversionFactory.create_conversion('CSVConversion')

        ConversionFactory.add_factory('ExtendedCSVConversion', CSVConversion)
        factories = ConversionFactory.factories

        self.assertEqual(len(factories), 3)
        self.assertTrue('CSVConversion' in factories)
        self.assertTrue('XMLConversion' in factories)
        self.assertTrue('ExtendedCSVConversion' in factories)

    def test_should_fail_if_exception_not_raised(self):
        with self.assertRaises(NameError):
            ConversionFactory.create_conversion('HTMLConversion')


class TestParser(unittest.TestCase):
    def test_inventory_item_parser(self):
        """
        Test that the parser returns the correct model
        """

        record = {
            'modifier_3_name': 'Large',
            'modifier_1_price': '-$0.25',
            'modifier_2_price': '$0.00',
            'modifier_2_name': 'Medium',
            'modifier_1_name': 'Small',
            'modifier_3_price': '$0.30',
            'cost': '$0.80',
            'description': 'Coffee',
            'quantity_on_hand': '100000',
            'price_type': 'system',
            'price': '$1.25',
            'item id': '111010'
        }

        expected_item = models.InventoryItem(id=111010, price=1.25, cost=0.80, description='Coffee',
                                             modifiers=[{'price': -0.25, 'name': 'Small'},
                                                        {'price': 0.0, 'name': 'Medium'},
                                                        {'price': 0.3, 'name': 'Large'}],
                                             price_type='system', quantity_on_hand=100000)

        item = parser.parse_inventory_item(record)

        self.assertEqual(item.id, expected_item.id)
        self.assertEqual(item.cost, expected_item.cost)
        self.assertEqual(item.description, expected_item.description)
        self.assertEqual(item.price_type, expected_item.price_type)
        self.assertEqual(item.quantity_on_hand, expected_item.quantity_on_hand)
        self.assertEqual(item.modifiers.sort(key=operator.itemgetter('price')),
                         expected_item.modifiers.sort(key=operator.itemgetter('price')))
        self.assertDictEqual(item.__dict__, expected_item.__dict__)


class TestFileIO(unittest.TestCase):
    def test_should_fail_if_not_valid_json(self):
        expected = json.dumps([{"simple_key": "simple_value"}], sort_keys=True, indent=2)

        models = [{'simple_key': 'simple_value'}]
        output = file_io.output_json(models)

        self.assertEqual(output, expected)


class TestValidationIntegers(unittest.TestCase):
    def test_should_fail_if_not_int(self):
        expected_value = 3
        value = validate.is_valid_int('3')
        self.assertEqual(expected_value, value)

    def test_should_fail_if_integer_is_not_int(self):
        expected_value = 3
        value = validate.is_valid_int(3)
        self.assertEqual(expected_value, value)

    def test_should_fail_if_float_is_not_none(self):
        value = validate.is_valid_int('3.0')
        self.assertIsNone(value)

    def test_should_fail_if_string_is_not_none(self):
        value = validate.is_valid_int('tree')
        self.assertIsNone(value)


class TestValidationFloats(unittest.TestCase):
    def test_should_fail_if_not_float(self):
        expected_value = 6.0
        value = validate.is_valid_float('6.0')
        self.assertEqual(expected_value, value)

    def test_should_fail_if_integer_is_not_float(self):
        expected_value = 6.0
        value = validate.is_valid_float(6)
        self.assertEqual(expected_value, value)

    def test_should_fail_if_float_is_not_valid_float(self):
        expected_value = 6.0
        value = validate.is_valid_float(6.0)
        self.assertEqual(expected_value, value)

    def test_should_fail_if_string_is_not_none(self):
        value = validate.is_valid_float("six")
        self.assertIsNone(value)


class TestValidationStrings(unittest.TestCase):
    def test_should_fail_if_not_string(self):
        expected_value = 'Coffee'
        value = validate.is_valid_string('Coffee')
        self.assertEqual(expected_value, value)

    def test_should_fail_if_integer_is_not_string(self):
        expected_value = '9'
        value = validate.is_valid_string(9)
        self.assertEqual(expected_value, value)

    def test_should_fail_if_float_not_string(self):
        expected_value = '9.0'
        value = validate.is_valid_string(9.0)
        self.assertEqual(expected_value, value)

    def test_should_fail_if_empty_string_not_string(self):
        expected_value = ''
        value = validate.is_valid_string('')
        self.assertEqual(expected_value, value)


class TestValidationPriceType(unittest.TestCase):
    def test_should_fail_if_price_type_not_open(self):
        expected_value = 'open'
        value = validate.is_valid_price_type('OPEN')
        self.assertEqual(expected_value, value)

    def test_should_fail_if_uppercase_price_type_not_open(self):
        expected_value = 'open'
        value = validate.is_valid_price_type('OPEN')
        self.assertEqual(expected_value, value)

    def test_should_fail_if_price_type_not_system(self):
        expected_value = 'system'
        value = validate.is_valid_price_type('system')
        self.assertEqual(expected_value, value)


class TestValidationConsistentKeys(unittest.TestCase):
    def test_should_fail_if_item_id_not_consistent_key(self):
        expected_value = 'item_id'
        value = validate.enforce_key_consistency('item id')
        self.assertEqual(expected_value, value)

    def test_should_fail_if_mixedcase_not_consistent_key(self):
        expected_value = 'item_id'
        value = validate.enforce_key_consistency('ITEM id')
        self.assertEqual(expected_value, value)

    def test_should_fail_if_cost_not_consistent_key(self):
        expected_value = 'cost'
        value = validate.enforce_key_consistency('cost')
        self.assertEqual(expected_value, value)


class TestValidationRegex(unittest.TestCase):
    def test_should_fail_if_not_valid_name_modifier(self):
        expected_values = ('modifier', '1', 'name')
        value = validate.regex_match_modifiers('modifier_1_name')
        self.assertEqual(expected_values, value)

    def test_should_fail_if_not_valid_price_modifier(self):
        expected_values = ('modifier', '1', 'price')
        value = validate.regex_match_modifiers('modifier_1_price')
        self.assertEqual(expected_values, value)

    def test_should_fail_if_regex_valid(self):
        value = validate.regex_match_modifiers('price_id')
        self.assertIsNone(value)


if __name__ == '__main__':
    unittest.main()
