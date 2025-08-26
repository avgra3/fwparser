"""Testing with large datasets for fwparser."""

from .create_fixedwidth_data import FixedWidthDataCreation
from fwparser.fwparser import parse_data_file

DEFINITIONS = {
    "customer_id": [0, 5],
    "first_name": [5, 10],
    "last_name": [15, 10],
    "address": [25, 50],
    "phone_number": [75, 10],
}
GENERATED_ROWS = 1_000_000
DATA = FixedWidthDataCreation(
    definitions=DEFINITIONS,
    generated_rows=GENERATED_ROWS,
)


def test_fw_data_generated():
    """Testing our helper class to generate data works.

    We test to make sure the returned object is of the correct type
    and to ensure the delimited and fixed width data sets have the
    same line count.
    """
    test_data = DATA.generate_data_file(delimiter="|")
    # We need to first verify we have the correct object
    assert isinstance(test_data, dict)
    delimited_data = test_data["delimited"]
    fixed_width_data = test_data["fixed_width"]
    delimited_line_count = len(delimited_data.split("\r\n"))
    fixed_width_line_count = len(fixed_width_data.split("\r\n"))
    # We generate a header row so the line count should be minus 1
    # for actual data rows.
    assert GENERATED_ROWS == delimited_line_count - 1
    assert GENERATED_ROWS == fixed_width_line_count - 1


def test_parse_data():
    """Testing parsing of large dataset."""
    data = DATA._fixed_width_and_delimited_line()
    fixed_width = data["fixed_width"]
    parsed_data = parse_data_file(
        raw_data_file=fixed_width,
        header_config=DEFINITIONS,
        trim_whitespace=False,
        offset=0,
        enclosed_by="",
    )
    header = ",".join(list(DEFINITIONS.keys())) + "\r\n"
    actual = header + data["delimited"]
    assert actual == parsed_data


def test_multiprocessing():
    """WORK IN PROGRESS"""
    assert 1 == 1
