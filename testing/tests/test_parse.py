"""All fwparser base tests."""

import unittest

from fwparser.errors import BadInputString
from fwparser.fwparser import (
    _get_column_names,
    _parse_data_by_line,
    _split_data,
    parse_data_file,
)
from testing.constants import DATA_OUTLINE, RAW_DATA


class Test_Parser(unittest.TestCase):
    """Fixed width parser."""

    def test_parse_data_with_extra_spaces(self):
        """Test parse with extra spaces."""
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
        """Parse data without spaces."""
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
        """Test line splits as expected."""
        expected = [
            "HERE IS LINE ONE",
            "HERE IS LINE TWO",
            "HERE IS LINE THREE",
        ]
        input01 = "./testing/tests/test_data.txt"
        actual01 = _split_data(raw_data_file=input01)
        self.assertEqual(expected, actual01)

    def test_get_column_names(self):
        """Test column names correctly extracted from definitions."""
        expected = [
            "customer_id",
            "first_name",
            "last_name",
            "address",
            "phone_number",
        ]
        actual01 = _get_column_names(header_config=DATA_OUTLINE)
        self.assertEqual(expected, actual01)
        # Test Out of order

    def test_bad_input_exception(self):
        """Confim error raised with bad inputs."""
        bad_input_not_string = 123

        with self.assertRaises(BadInputString):
            _split_data(bad_input_not_string)

    def test_raw_has_enclosed(self):
        """Test raw data is enclosed."""
        raw = "Henry               Conrad, MD          "
        config = {"first_name": (0, 20), "last_name": (20, 20)}
        expected = '"first_name","last_name"\r\n"Henry","Conrad, MD"'
        actual = parse_data_file(
            raw_data_file=raw,
            header_config=config,
            trim_whitespace=True,
            offset=0,
            enclosed_by='"',
        )
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
