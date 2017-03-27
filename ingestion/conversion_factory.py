#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
conversion_factory
----------------------------------
Polymorphic factory allowing providing a standard interface for extracting file contents,
parsing from one type to an intermediary state, and serialising the output to a sandarised format
"""

from ingestion import file_io
from ingestion import parser


class ConversionFactory:
    """ Polymorphic factory allowing creation of new Conversions"""
    factories = {}

    def add_factory(id, factory):
        """ Allows new conversion factories to be added """
        ConversionFactory.factories[id] = factory

    add_factory = staticmethod(add_factory)

    def create_conversion(id):
        """ Provides creation of conversion factories """
        if id not in ConversionFactory.factories:
            ConversionFactory.factories[id] = eval(id + '.Factory()')
        return ConversionFactory.factories[id].create()

    create_conversion = staticmethod(create_conversion)


class Conversion(object):
    """ Abstract base class for Conversion factory """
    pass


class CSVConversion(Conversion):
    """ CSV Conversion Factory """

    def __init__(self):
        self.input_file = None
        self.output_file = None
        self.records = []
        self.models = []

    def set_input_file(self, input_file):
        """ sets the csv input file """
        self.input_file = input_file

    def set_output_file(self, output_file):
        """ sets the json output file """
        self.output_file = output_file

    def execute(self):
        """ converts input csv file to json output file """
        self._extract()
        self._parse()
        self._transform()

    def _extract(self):
        """ extracts the contents of the csv file to a list of records """
        if self.input_file is None:
            raise FileNotFoundError()

        self.records = file_io.read_csv(self.input_file)

    def _parse(self):
        """ parses a list of records into a list of models """
        self.models = [parser.parse_inventory_item(record) for record in self.records]

    def _transform(self):
        """ serialises a list of models to an output json file """
        data = file_io.output_json(self.models)
        file_io.write_json(self.output_file, data)

    class Factory:
        """ Allows instantization of factory """

        def create(self):
            """ creates CSV Conversion factory"""
            return CSVConversion()


class XMLConversion(Conversion):
    """ XML Conversion Factory """

    def __init__(self):
        self.input_file = None
        self.output_file = None
        self.records = []
        self.models = []

    def set_input_file(self, input_file):
        """ sets the xml input file """
        self.input_file = input_file

    def set_output_file(self, output_file):
        """ sets the json output file """
        self.output_file = output_file

    def execute(self):
        """ extracts the contents of the csv file to a list of records """
        self._extract()
        self._parse()
        self._transform()

    def _extract(self):
        """ extracts the contents of the csv file to a list of records """
        raise NotImplementedError

    def _parse(self):
        """ parses a list of records into a list of models """
        raise NotImplementedError

    def _transform(self):
        """ serialises a list of models to an output json file """
        raise NotImplementedError

    class Factory:
        """ Allows instantization of factory """

        def create(self):
            """ creates XML Conversion factory"""
            return XMLConversion()
