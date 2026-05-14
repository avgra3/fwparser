from fwparser.fwparser import parse_data_file

from .create_fixedwidth_data import FixedWidthDataCreation

DEFINITIONS = {
    "customer_id": (0, 5),
    "first_name": (5, 10),
    "last_name": (15, 10),
    "address": (25, 50),
    "phone_number": (75, 10),
}
GENERATED_ROWS = 1_000
DELIMITER = "|"
LINE_TERMINATOR = "\r\n"
DATA = FixedWidthDataCreation(
    definitions=DEFINITIONS,
    delimiter=DELIMITER,
    generated_rows=GENERATED_ROWS,
    line_terminator=LINE_TERMINATOR,
)


def test_fw_data_generated():
    """Testing our helper class to generate data works.

    We test to make sure the returned object is of the correct type
    and to ensure the delimited and fixed width data sets have the
    same line count.
    """
    test_data = DATA.generate_data_file()
    # We need to first verify we have the correct object
    assert isinstance(test_data, dict)
    delimited_data = test_data["delimited"]
    fixed_width_data = test_data["fixed_width"]
    delimited_line_count = len(delimited_data.split(LINE_TERMINATOR))
    fixed_width_line_count = len(fixed_width_data.split(LINE_TERMINATOR))
    # We generate a header row so the line count should be minus 1
    # for actual data rows.
    assert delimited_line_count - 1 == GENERATED_ROWS
    assert fixed_width_line_count - 1 == GENERATED_ROWS


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
        delimiter=DELIMITER,
    )
    header = f"{DELIMITER}".join(list(DEFINITIONS.keys())) + "\r\n"
    actual = header + data["delimited"]
    assert actual == parsed_data
