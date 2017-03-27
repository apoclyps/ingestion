## Ingestion

Ingestion is a Python package for converting specific CSVs to other formats. At present only inventory items CSVs are supported. It is expected that other formats will be added very soon (such as customers, and transactions) and should require as little work as possible to incorporate into the package.

### Overview

This solution has been implemented using a polymorphic factory (ConversionFactory.py) to abstract the reading/writing of data between formats (using file_io.py).

An intermediary model has been used to ensure the data conforms to a standard whilst allowing it to easily be converted to and from other formats/ data structures with minimal amount of work required.

Simple validation (validate.py) is performed on each property (within parser.py) before the value is stored. Price modifiers are an exception; each price modifier field is validated and stored within a temporary dictionary until all record values have been processed. Once all modifiers have been processed the modifiers property will be set.

The following sequence diagram provides an overview of the service:

![ScreenShot](/ingestion_data_flow.png?raw=true "Ingestion Data Flow")

### Assumptions

- The ordering of the object values within the output JSON is irrelevant as it will be interpreted the same way regardless of how the object's values are ordered.
- The price, cost, and quantity_on_hand values should be output as null if a value has not been set instead of defaulting to 0 to match the example.json.
- The description object value should contain only alpha characters as the incrementing numeric value in the CSV description field does not appear to hold any relevance to the description.
- The item id field within the csv should map to id.

### Project Structure
├── LICENSE <br />
├── README.md <br />
├── dev-requirements.txt <br />
├── example.csv <br />
├── example.json <br />
├── ingestion <br />
│   ├── __init__.py <br />
│   ├── conversion_factory.py <br />
│   ├── file_io.py <br />
│   ├── models.py <br />
│   ├── parser.py <br />
│   └── validate.py <br />
├── main.py <br />
├── requirements.txt <br />
├── setup.py <br />
└── test s<br />
    ├── __init__.py <br />
        └── tests_ingestion.py <br />

## Dependencies
For development, please install the dev-requirements.txt if you would like to run linting and coverage reports. Otherwise, there are no external dependencies other than setup tools and python 3.5.2

```
pip install -r dev-reqirements.txt
```

## Installation
Clone the repository and install via setup tools

```
python setup.py install
```

## Running the conversion
To run the example within the repository you can use the following command:

```
python main.py -i example.csv -o example.json
```

Running the above command produce the following output:
[![asciicast](https://asciinema.org/a/1b07156uk683bt8hv25fmv7w7.png)](https://asciinema.org/a/1b07156uk683bt8hv25fmv7w7)

## Tests
The simplest way to run the test suite (assuming you have setuptools installed) is via the following:

```
python setup.py test
```

Running the above command produces the following output:
[![asciicast](https://asciinema.org/a/4rdetn4g9kr1qj73kn35tozm6.png)](https://asciinema.org/a/4rdetn4g9kr1qj73kn35tozm6)

### Code Coverage
To view code coverage of the ingestion package, please run the following:

```
pip install -r dev-requirements.txt

coverage run main.py -i example.csv -o example.json
coverage report
coverage html
```

Alternatively coverage can also be viewed online : [Coverage Report](http://ingestion-coverage.s3-website-eu-west-1.amazonaws.com)

### Linting
To view linting for the ingestion package, please run the following:

```
pylint ingestion
```

If you would prefer to view an existing report you can view it here : [Coverage Report](http://ingestion-coverage.s3-website-eu-west-1.amazonaws.com)

## License
Free software: http://unlicense.org/
