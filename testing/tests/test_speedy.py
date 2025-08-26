from fwparser.speedy import FastFwparser
from fwparser.fwparser import parse_data_file
from fwparser.errors import NotEnoughCpus
from testing.create_fixedwidth_data import FixedWidthDataCreation
import pytest

LINE_ENDING = "\r\n"
DELIMITER = "|"
DEFINITIONS = {
    "customer_id": [0, 5],
    "first_name": [5, 10],
    "last_name": [15, 10],
    "address": [25, 50],
    "phone_number": [75, 10],
}
GENERATED_ROWS = 8
OFFSET = 0
TRIM_WHITESPACE = False
ENCLOSED_BY = ""
MAX_CPUS = 4
DATA = FixedWidthDataCreation(
    definitions=DEFINITIONS,
    generated_rows=GENERATED_ROWS,
    line_terminator=LINE_ENDING,
    delimiter=DELIMITER,
)


def test_mulitiprocessing_correct():
    test_data = DATA.generate_data_file()
    fixed_width = test_data["fixed_width"]
    fw_slow_parse = parse_data_file(
        raw_data_file=fixed_width,
        header_config=DEFINITIONS,
        trim_whitespace=TRIM_WHITESPACE,
        offset=OFFSET,
        enclosed_by=ENCLOSED_BY,
        delimiter=DELIMITER,
        line_ending=LINE_ENDING,
    )

    fastFwparser = FastFwparser(
        data=fixed_width,
        header_config=DEFINITIONS,
        trim_whitespace=TRIM_WHITESPACE,
        sep=DELIMITER,
        offset=OFFSET,
        enclosed_by=ENCLOSED_BY,
        line_ending=LINE_ENDING,
        max_cpu=MAX_CPUS,
    )
    fw_fast_parse = fastFwparser.parse_data_file()
    fw_fast_parse_set = set(fw_fast_parse.split(LINE_ENDING))
    fw_slow_parse_set = set(fw_slow_parse.split(LINE_ENDING))

    assert fw_fast_parse_set.issubset(fw_slow_parse_set)
    assert fw_slow_parse_set.issubset(fw_fast_parse_set)
    assert fw_fast_parse == fw_slow_parse


def test_not_enough_cpus():
    BAD_CPU_COUNT = 1
    test_data = DATA.generate_data_file()
    fixed_width = test_data["fixed_width"]
    with pytest.raises(NotEnoughCpus):
        FastFwparser(
            data=fixed_width,
            header_config=DEFINITIONS,
            trim_whitespace=TRIM_WHITESPACE,
            sep=DELIMITER,
            offset=OFFSET,
            enclosed_by=ENCLOSED_BY,
            line_ending=LINE_ENDING,
            max_cpu=BAD_CPU_COUNT,
        )
