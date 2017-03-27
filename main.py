#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main
----------------------------------
An entry point to using the ingestion package
"""

import sys
import getopt
import os

from ingestion.conversion_factory import ConversionFactory

CSV_CONVERSION = 'CSVConversion'
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def main(argv):
    """ Accepts CLI arguments for an CSV input file and outputs data as a JSON file """
    input_file = ''
    output_file = ''
    try:
        opts, _ = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <input_file> -o <output_file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    if input_file == '' or output_file == '':
        raise Exception('Please provide an input and outfile e.g. python -i example.csv -o example.json')

    print('Converting file %s to %s' % (input_file, output_file))

    file_import = ConversionFactory.create_conversion(CSV_CONVERSION)
    file_import.set_input_file(PROJECT_ROOT + '/' + input_file)
    file_import.set_output_file(PROJECT_ROOT + '/' + output_file)
    file_import.execute()

    print('Conversion Complete')


if __name__ == "__main__":
    main(sys.argv[1:])
