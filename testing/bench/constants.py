from datetime import datetime
from multiprocessing import cpu_count
from pathlib import Path

from cpuinfo import get_cpu_info

# Basic CPU info
CPU_INFO = get_cpu_info()
CPU_NAME = CPU_INFO["brand_raw"]
CPU_COUNT = cpu_count()

# Setting up fixed width data
DEFINITIONS = {
    "customer_id": [0, 5],
    "first_name": [5, 10],
    "last_name": [15, 10],
    "address": [25, 50],
    "phone_number": [75, 10],
}

GENERATED_ROWS = 1_000_000
DELIMITER = "|"
LINE_TERMINATOR = "\r\n"
TRIM_WHITESPACE = True
OFFSET = 0
ENCLOSED_BY = ""

# CSV specific Parameters
DATE = datetime.now().strftime("%Y-%m-%d")
CSV_NAME = Path.cwd() / "Benchmark_Results" / "bench_mark.csv"
HEADER = [
    "function_name",
    "generated_rows",
    "execution_time_seconds",
    "cpu_name",
    "cpu_count",
    "run_number",
    "date_ran",
]


# Simulated Data File Name
RAW_DATA_FILE = Path.cwd() / "testing/bench/raw_data_file.txt"
RUNS = 100
