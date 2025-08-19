"""All tests with Pandas and fwparser."""

import unittest
from io import StringIO
import pandas as pd
from .constants import RAW_DATA, DATA_OUTLINE

from fwparser.fwparser import (
    parse_data_file,
)
from fwparser.pandas import parse_to_pandas


class Test_Parser_and_Pandas(unittest.TestCase):
    """Test to confirm parser works with Pandas as expected."""

    def test_parse_data_with_extra_spaces(self):
        """Test parse data with extra spaces."""
        data = {
            "customer_id": ["12345"],
            "first_name": ["John"],
            "last_name": ["Doe"],
            "address": ["123 Main St"],
            "phone_number": ["1234567890"],
        }

        df_test = pd.DataFrame(data)
        actual = parse_data_file(
            raw_data_file=RAW_DATA,
            header_config=DATA_OUTLINE,
            trim_whitespace=True,
            offset=0,
            enclosed_by="",
        )
        actual_df = pd.read_csv(
            StringIO(actual),
            header=0,
            dtype="str",
            sep=",",
        )
        result = df_test.equals(actual_df)

        self.assertEqual(result, True)

    def test_parse_data_enclosed_by(self):
        """Test parsing of enclosed data."""
        raw = "Henry               Conrad, MD          "
        data = {
            "first_name": ["Henry"],
            "last_name": ["Conrad, MD"],
        }
        config = {"first_name": (0, 20), "last_name": (20, 20)}
        df_test = pd.DataFrame(data)
        actual_df = parse_to_pandas(
            raw_data_file=raw,
            header_config=config,
            trim_white_space=True,
            enclosed_by="'",
        )
        result = df_test.equals(actual_df)
        self.assertEqual(result, True)


if __name__ == "__main__":
    unittest.main()
