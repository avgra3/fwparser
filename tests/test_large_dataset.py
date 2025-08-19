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

DATA = FixedWidthDataCreation(
    definitions=DEFINITIONS,
    generated_rows=1_000_000_000,
)


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
