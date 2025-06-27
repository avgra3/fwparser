import unittest
import sys
from io import StringIO
import pandas as pd

sys.path.append("..")

from fwparser.fwparser import (
    _get_column_names,
    _parse_data_by_line,
    _parse_all_data,
    _split_data,
    parse_data_file,
)
from fwparser.pandas import parse_to_pandas


RAW_DATA = "12345John      Doe       123 Main St         1234567890"
DATA_OUTLINE = {
    "customer_id": (0, 5),
    "first_name": (5, 10),
    "last_name": (15, 10),
    "address": (25, 20),
    "phone_number": (45, 10),
}


class Test_Parser_and_Pandas(unittest.TestCase):
    def test_parse_data_with_extra_spaces(self):
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
        actual_df = pd.read_csv(StringIO(actual), header=0, dtype="str", sep=",")
        result = df_test.equals(actual_df)

        self.assertEqual(result, True)
    
    def test_parse_data_enclosed_by(self):
        raw = f"Henry               Conrad, MD          "
        data = {
            "first_name": ["Henry"],
            "last_name": ["Conrad, MD"],
        }
        config = {"first_name": (0, 20), "last_name": (20, 20)}
        df_test = pd.DataFrame(data)
        actual_df = parse_to_pandas(raw_data_file=raw, header_config=config, trim_white_space=True, enclosed_by="'")
        result = df_test.equals(actual_df)
        self.assertEqual(result, True)


if __name__ == "__main__":
    unittest.main()
