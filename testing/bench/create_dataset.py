from testing.create_fixedwidth_data import FixedWidthDataCreation
from .constants import (
    DEFINITIONS,
    DELIMITER,
    GENERATED_ROWS,
    LINE_TERMINATOR,
    RAW_DATA_FILE,
)


def create_dataset() -> None:
    DATA = FixedWidthDataCreation(
        definitions=DEFINITIONS,
        delimiter=DELIMITER,
        generated_rows=GENERATED_ROWS,
        line_terminator=LINE_TERMINATOR,
    ).generate_data_file()
    FIXED_WIDTH = DATA["fixed_width"]

    with open(RAW_DATA_FILE, "w") as file:
        file.write(FIXED_WIDTH)
