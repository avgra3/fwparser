"""Performance comparisons between our single core process and multi-core process"""

import csv
from pathlib import Path
from time import perf_counter

from fwparser.fwparser import parse_data_file
from fwparser.speedy import FastFwparser

from .constants import (
    CPU_COUNT,
    CPU_NAME,
    CSV_NAME,
    DATE,
    DEFINITIONS,
    DELIMITER,
    ENCLOSED_BY,
    GENERATED_ROWS,
    HEADER,
    LINE_TERMINATOR,
    OFFSET,
    RAW_DATA_FILE,
    RUNS,
    TRIM_WHITESPACE,
)
from .create_dataset import create_dataset


def test_cores():
    create_output(max_cores_to_use=CPU_COUNT)
    assert Path.exists(CSV_NAME)


def create_output(max_cores_to_use: int):
    if not Path.exists(RAW_DATA_FILE):
        print(f"File `{RAW_DATA_FILE}` doesn't currently exist. Making now.")
        create_dataset()
    print(f"Starting write to csv at {CSV_NAME}")
    if not Path.exists(CSV_NAME):
        with open(CSV_NAME, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=DELIMITER)
            writer.writerow(HEADER)

    with open(CSV_NAME, "a") as file:
        for i in range(RUNS):
            run_num = i + 1
            print(f"Starting run number {run_num}")
            single_parser_results = single_parser(run_number=run_num)
            file.write(single_parser_results)
            for j in range(1, max_cores_to_use + 1):
                print(f"Starting multiprocessing core test: {j} Cores being used")
                mp_parser_results = mp_parser(cpus_used=j, run_number=run_num)
                file.write(mp_parser_results)


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
        "1",
        f"{run_number}",
        f"{DATE}",
    ]
    print("Finishing single_parser")
    return f"{DELIMITER}".join(results) + LINE_TERMINATOR


def mp_parser(cpus_used: int, run_number: int) -> str:
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
        max_cpu=cpus_used,
    ).parse_data_file()
    end = perf_counter()
    elapsed = end - start
    results = [
        "mp_parser",
        f"{GENERATED_ROWS}",
        f"{elapsed}",
        f"{CPU_NAME}",
        f"{cpus_used}",
        f"{run_number}",
        f"{DATE}",
    ]
    print("Finishing mp_parser")
    return f"{DELIMITER}".join(results) + LINE_TERMINATOR
