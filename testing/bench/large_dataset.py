"""Performance comparisons between our single core process and multi-core process"""

from time import perf_counter
import csv
from fwparser.fwparser import parse_data_file
from fwparser.speedy import FastFwparser
from pathlib import Path
from .constants import (
    GENERATED_ROWS,
    DELIMITER,
    LINE_TERMINATOR,
    TRIM_WHITESPACE,
    OFFSET,
    ENCLOSED_BY,
    CSV_NAME,
    HEADER,
    RAW_DATA_FILE,
    DEFINITIONS,
    CPU_COUNT,
    CPU_NAME,
)
from .create_dataset import create_dataset

RUNS = 100


def test_create_output():
    if not Path.exists(RAW_DATA_FILE):
        print(f"File `{RAW_DATA_FILE}` doesn't currently exist. Making now.")
        create_dataset()
    print(f"Starting write to csv at {CSV_NAME}")
    with open(CSV_NAME, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=DELIMITER)
        writer.writerow(HEADER)

    with open(CSV_NAME, "a") as file:
        for i in range(RUNS):
            run_num = i + 1
            print(f"Starting run number {run_num}")
            single_parser_results = single_parser(run_number=run_num)
            mp_parser_results = mp_parser(run_number=run_num)
            file.write(single_parser_results)
            file.write(mp_parser_results)
    assert Path.exists(CSV_NAME)


def single_parser(run_number: int) -> str:
    print("Running single_parser")
    start = perf_counter()
    parse_data_file(
        raw_data_file=RAW_DATA_FILE,
        header_config=DEFINITIONS,
        trim_whitespace=TRIM_WHITESPACE,
        offset=OFFSET,
        enclosed_by=ENCLOSED_BY,
    )
    end = perf_counter()
    elapsed = end - start
    results = [
        "single_parser",
        f"{GENERATED_ROWS}",
        f"{elapsed}",
        f"{CPU_NAME}",
        f"{CPU_COUNT}",
        f"{run_number}",
    ]
    print("Finishing single_parser")
    return f"{DELIMITER}".join(results) + LINE_TERMINATOR


def mp_parser(run_number: int) -> str:
    print("Starting mp_parser")
    start = perf_counter()
    FastFwparser(
        data=RAW_DATA_FILE,
        header_config=DEFINITIONS,
        trim_whitespace=TRIM_WHITESPACE,
        sep=DELIMITER,
        offset=OFFSET,
        enclosed_by=ENCLOSED_BY,
        line_ending=LINE_TERMINATOR,
        max_cpu=CPU_COUNT,
    ).parse_data_file()
    end = perf_counter()
    elapsed = end - start
    results = [
        "mp_parser",
        f"{GENERATED_ROWS}",
        f"{elapsed}",
        f"{CPU_NAME}",
        f"{CPU_COUNT}",
        f"{run_number}",
    ]
    print("Starting mp_parser")
    return f"{DELIMITER}".join(results) + LINE_TERMINATOR
