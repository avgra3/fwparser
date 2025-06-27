import unittest
import sys

sys.path.append("..")

from fwparser.fwparser import (
    _get_column_names,
    _parse_data_by_line,
    _parse_all_data,
    _split_data,
    parse_data_file,
)
from fwparser.toml_parser import (
    _get_configuration,
    _get_definitions,
    _turn_lists_to_tuples,
    toml_parse_data_file,
)

VALID_TEST_TOML = "./test/test_valid_toml.toml"
INVALID_TEST_TOMLS = ["./test/test_invalid_toml.toml", "INVALID_TEST", "NOT_TOML"]
RAW_DATA = "12345John      Doe       123 Main St         1234567890"


class Test_Parser_with_Toml(unittest.TestCase):
    def test_toml_parse_data_file(self):
        config_path = "test/test_toml.toml"
        expected = "customer_id,first_name,last_name,address,phone_number\r\n12345,John,Doe,123 Main St,1234567890\r\n"
        actual = toml_parse_data_file(
            raw_data_file=RAW_DATA,
            toml_file_path=config_path,
            trim_whitespace=True,
            offset=0,
        )
        self.assertEqual(expected, actual)

    def test_turn_list_to_tuples(self):
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
        valid_input = {"definitions": {"Column": (0, 5)}}
        invalid_input = {"random": {"Column": (0, 5)}}
        valid_expected = {"Column": (0, 5)}
        self.assertDictEqual(valid_expected, _get_definitions(valid_input))
        with self.assertRaises(Exception):
            _get_definitions(invalid_input)

    def test_get_configuration_valid(self):
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
        for file in INVALID_TEST_TOMLS:
            with self.assertRaises(Exception):
                _get_configuration(file)


if __name__ == "__main__":
    unittest.main()
