"""Testing with large datasets for fwparser."""

from testing.create_fixedwidth_data import FixedWidthDataCreation
from fwparser.fwparser import parse_data_file
from fwparser.speedy import FastFwparser
from platform import processor
import csv
import datetime
from multiprocessing import cpu_count

DEFINITIONS = {
    "customer_id": [0, 5],
    "first_name": [5, 10],
    "last_name": [15, 10],
    "address": [25, 50],
    "phone_number": [75, 10],
}
GENERATED_ROWS = 1_000_000_000
DELIMITER = "|"
LINE_TERMINATOR = "\r\n"
TRIM_WHITESPACE = True
OFFSET = 0
ENCLOSED_BY = ""
DATA = FixedWidthDataCreation(
    definitions=DEFINITIONS,
    delimiter=DELIMITER,
    generated_rows=GENERATED_ROWS,
    line_terminator=LINE_TERMINATOR,
).generate_data_file()
FIXED_WIDTH = DATA["fixed_width"]
CPU_NAME = processor()
CPU_COUNT = cpu_count()
# CSV
DATE = datetime.datetime.now()
CSV_NAME = "bench_mark_{DATE}.csv"
HEADER = [
    "function_name",
    "generated_rows",
    "execution_time_seconds",
    "cpu_name",
    "cpu_count",
    "run_number",
]
RUNS = 10


def create_output():
    with open(CSV_NAME, "w", newline=LINE_TERMINATOR) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(f"{DELIMITER}".join(HEADER))

        for i in range(RUNS):
            single_parser_results = single_parser(run_number=i)
            mp_parser_results = mp_parser(run_number=i)
            result = [single_parser_results, mp_parser_results]
            writer.writerows(result)


def single_parser(run_number: int) -> str:
    start = datetime.datetime.now()
    parse_data_file(
        raw_data_file=DATA,
        header_config=DEFINITIONS,
        trim_whitespace=TRIM_WHITESPACE,
        offset=OFFSET,
        enclosed_by=ENCLOSED_BY,
    )
    end = datetime.date.now()
    elapsed = end - start
    results = [
        "single_parser",
        f"{GENERATED_ROWS}",
        f"{elapsed}",
        f"{CPU_NAME}",
        f"{CPU_COUNT}",
        f"{run_number}",
    ]
    return f"{DELIMITER}".join(results)


def mp_parser(run_number: int) -> str:
    start = datetime.datetime.now()
    FastFwparser(
        data=DATA,
        header_config=DEFINITIONS,
        trim_whitespace=TRIM_WHITESPACE,
        sep=DELIMITER,
        offset=OFFSET,
        enclosed_by=ENCLOSED_BY,
        line_ending=LINE_TERMINATOR,
        max_cpu=CPU_COUNT,
    ).parse_data_file()
    end = datetime.date.now()
    elapsed = end - start
    results = [
        "mp_parser",
        f"{GENERATED_ROWS}",
        f"{elapsed}",
        f"{CPU_NAME}",
        f"{CPU_COUNT}",
        f"{run_number}",
    ]
    return f"{DELIMITER}".join(results)
