#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
file_io
----------------------------------
Generic IO for reading and writing to files
"""

import csv

import json


def read_csv(file):
    """ Reads a csv file and returns all rows (including field names) """
    with open(file, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        rows = [row for row in reader]
        return rows


def write_json(file, data):
    """ Reads a csv file and returns all rows (including field names) """
    with open(file, 'w') as outfile:
        outfile.write(data)


class CustomModelEncoder(json.JSONEncoder):
    """ Customer JSON Encoder used to strip _ from model properties """

    def default(self, o):
        return {key.lstrip('_'): value for key, value in vars(o).items()}


def output_json(models):
    """ Converts object and all properties to valid json with keys sorted """
    return json.dumps(models, cls=CustomModelEncoder, sort_keys=True, indent=2)
