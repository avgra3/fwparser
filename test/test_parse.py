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


RAW_DATA = "12345John      Doe       123 Main St         1234567890"
DATA_OUTLINE = {
    "customer_id": (0, 5),
    "first_name": (5, 10),
    "last_name": (15, 10),
    "address": (25, 20),
    "phone_number": (45, 10),
}


class Test_Parser(unittest.TestCase):
    def test_parse_data_with_extra_spaces(self):
        expected = {
            "customer_id": "12345",
            "first_name": "John" + " " * 6,
            "last_name": "Doe" + " " * 7,
            "address": "123 Main St" + " " * 9,
            "phone_number": "1234567890",
        }
        actual = _parse_data_by_line(
            header_config=DATA_OUTLINE,
            raw_data_line=RAW_DATA,
            trim_whitespace=False,
        )
        self.assertEqual(actual, expected)

    def test_parse_data_without_extra_spaces(self):
        expected = {
            "customer_id": "12345",
            "first_name": "John",
            "last_name": "Doe",
            "address": "123 Main St",
            "phone_number": "1234567890",
        }
        actual = _parse_data_by_line(
            header_config=DATA_OUTLINE,
            raw_data_line=RAW_DATA,
            trim_whitespace=True,
        )
        self.assertEqual(actual, expected)

    def test_line_split(self):
        expected = ["HERE IS LINE ONE", "HERE IS LINE TWO", "HERE IS LINE THREE"]
        input01 = "./test/test_data.txt"
        actual01 = _split_data(raw_data_file=input01)
        self.assertEqual(expected, actual01)

    def test_get_column_names(self):
        expected = ["customer_id", "first_name", "last_name", "address", "phone_number"]
        actual01 = _get_column_names(header_config=DATA_OUTLINE)
        self.assertEqual(expected, actual01)
        # Test Out of order
        input02 = {
            "address": (25, 20),
            "first_name": (5, 10),
            "customer_id": (0, 5),
            "phone_number": (45, 10),
            "last_name": (15, 10),
        }

    def test_bad_input_exception(self):
        bad_input_not_string = 123

        with self.assertRaises(Exception):
            _split_data(bad_input_not_string)


if __name__ == "__main__":
    unittest.main()
