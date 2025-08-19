"""All tests for Parsing Toml files with fwparser."""

import unittest
from .constants import VALID_TEST_TOML, INVALID_TEST_TOMLS, RAW_DATA

from fwparser.toml_parser import (
    _get_configuration,
    _get_definitions,
    _turn_lists_to_tuples,
    toml_parse_data_file,
)


class Test_Parser_with_Toml(unittest.TestCase):
    """Testing of Parsing with Toml files."""

    def test_toml_parse_data_file(self):
        """Tests toml parsing."""
        config_path = "tests/test_toml.toml"
        expected = "customer_id,first_name,last_name,address,phone_number\r\n12345,John,Doe,123 Main St,1234567890"  # noqa: E501
        actual = toml_parse_data_file(
            raw_data_file=RAW_DATA,
            toml_file_path=config_path,
            trim_whitespace=True,
            offset=0,
        )
        self.assertEqual(expected, actual)

    def test_turn_list_to_tuples(self):
        """Confirms dictionary is correctly created."""
        expected = {
            "customer_id": (0, 15),
            "first_name": (5, 10),
            "last_name": (15, 10),
            "address": (25, 20),
            "phone_number": (45, 10),
        }

        input = {
            "customer_id": [0, 15],
            "first_name": [5, 10],
            "last_name": [15, 10],
            "address": [25, 20],
            "phone_number": [45, 10],
        }

        test = _turn_lists_to_tuples(input)
        self.assertDictEqual(test, expected)

    def test_get_definitions_valid(self):
        """Verifies that provided definitions are valid.

        Will error if there is an invalid input.
        """
        valid_input = {"definitions": {"Column": (0, 5)}}
        invalid_input = {"random": {"Column": (0, 5)}}
        valid_expected = {"Column": (0, 5)}
        self.assertDictEqual(valid_expected, _get_definitions(valid_input))
        with self.assertRaises(Exception):
            _get_definitions(invalid_input)

    def test_get_configuration_valid(self):
        """Tests that the congiguration provided is valid.

        If the passed configuration is invalid, error.
        """
        actual = _get_configuration(VALID_TEST_TOML)
        expected = {
            "definitions": {
                "customer_id": [0, 15],
                "first_name": [5, 10],
                "last_name": [15, 10],
                "address": [25, 20],
                "phone_number": [45, 10],
            }
        }
        self.assertDictEqual(actual, expected)

    def test_get_configuration_throws(self):
        """Verify an invalid toml file throws an exception."""
        for file in INVALID_TEST_TOMLS:
            with self.assertRaises(Exception):
                _get_configuration(file)


if __name__ == "__main__":
    unittest.main()
