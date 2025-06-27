import polars as pl

import unittest
import sys
from io import StringIO

sys.path.append("..")

from fwparser.fwparser import (
    _get_column_names,
    _parse_data_by_line,
    _parse_all_data,
    _split_data,
    parse_data_file,
)
from fwparser.polars import parse_to_polars


RAW_DATA = "12345John      Doe       123 Main St         1234567890"
DATA_OUTLINE = {
    "customer_id": (0, 5),
    "first_name": (5, 10),
    "last_name": (15, 10),
    "address": (25, 20),
    "phone_number": (45, 10),
}


class Test_Parser_and_Polars(unittest.TestCase):
    def test_parse_data_with_extra_spaces(self):
        data = {
            "customer_id": ["12345"],
            "first_name": ["John"],
            "last_name": ["Doe"],
            "address": ["123 Main St"],
            "phone_number": ["1234567890"],
        }

        df_test = pl.from_dict(data)
        actual = parse_data_file(
            raw_data_file=RAW_DATA,
            header_config=DATA_OUTLINE,
            trim_whitespace=True,
            offset=0,
        )
        actual_df = pl.read_csv(
            StringIO(actual), has_header=True, separator=",", infer_schema=False
        )
        result = df_test.equals(actual_df)

        self.assertEqual(result, True)

    def test_enclosed_by(self):
        data = {
            "customer_id": ["12345"],
            "first_name": ["J,hn"],
            "last_name": ["Doe"],
            "address": ["123 Main St"],
            "phone_number": ["1234567890"],
        }
        raw_data = "12345J,hn      Doe       123 Main St         1234567890"

        df_test = pl.from_dict(data)
        df_actual = parse_to_polars(raw_data_file=raw_data, header_config=DATA_OUTLINE, trim_white_space=True, offset=0, using_toml=False, enclosed_by="'")
        result = df_test.equals(df_actual)
        self.assertEqual(result, True)

if __name__ == "__main__":
    unittest.main()
