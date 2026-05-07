"""fwparser tools for converting fixed witdth files to delimited."""

import os
from typing import Generator
from .errors import BadInputString, IndexOutOfBoundsError


def _get_column_names(header_config: dict[str, tuple]) -> list[str]:
    """Extract and sort column names by their start position."""
    header_order = [(key, header_config[key][0]) for key in header_config]
    _sorted = sorted(header_order, key=lambda x: x[1])
    return [item[0] for item in _sorted]


def _parse_data_by_line(
    header_config: dict[str, tuple],
    raw_data_line: str,
    trim_whitespace: bool = False,
    offset: int = 0,
) -> dict[str, str]:
    """Parse a single line into a dict using fixed-width positions."""
    parsed_field = {}
    for header, (start, length) in header_config.items():
        value_start = int(start) - offset
        if value_start < 0:
            raise IndexOutOfBoundsError(field_name=header)

        value_end = value_start + int(length)
        data = raw_data_line[value_start:value_end]

        parsed_field[header] = data.strip() if trim_whitespace else data

    return parsed_field


def _parse_all_data(
    all_data: list[str],
    header_config: dict[str, tuple],
    trim_whitespace: bool = False,
    offset: int = 0,
) -> list[dict[str, str]]:
    result = []
    for line in all_data:
        row_data = _parse_data_by_line(
            header_config=header_config,
            raw_data_line=line,
            trim_whitespace=trim_whitespace,
            offset=offset,
        )
        result.append(row_data)
    return result


def _split_data(raw_data_file: str) -> list[str]:
    if os.path.isfile(raw_data_file):
        with open(raw_data_file) as file:
            data = file.read().splitlines()
        return data
    if os.path.isdir(raw_data_file):
        message = f'The filepath, "{raw_data_file}", you put is a directory...'
        raise BadInputString(message)
    if isinstance(raw_data_file, str):
        data = raw_data_file.splitlines()
        return data
    message = f"""The raw data path you included is not a file path or of type string:
    {raw_data_file}
    """
    raise BadInputString(message)


def _get_line_iterator(raw_data_file: str) -> Generator[str, None, None]:
    """Return an iterator over lines, avoiding loading the entire file into memory when possible."""
    if os.path.isfile(raw_data_file):
        with open(raw_data_file, encoding="utf-8", errors="replace") as file:
            yield from (line.rstrip("\r\n") for line in file)  # normalize line endings
        return

    if os.path.isdir(raw_data_file):
        raise BadInputString(f'The filepath "{raw_data_file}" is a directory.')

    if isinstance(raw_data_file, str):
        yield from (line.rstrip("\r\n") for line in raw_data_file.splitlines())
        return

    raise BadInputString(
        f"The raw data path you included is not a file path or string:\n{raw_data_file}"
    )


def parse_data_file(
    raw_data_file: str,
    header_config: dict[str, tuple],
    trim_whitespace: bool = False,
    offset: int = 0,
    enclosed_by: str = "",
    delimiter: str = ",",
    line_ending: str = "\r\n",
) -> str:
    """Parse fixed-width data file and return CSV-like string.

    Memory improvements:
      - Streams input line-by-line (no full file in memory for files)
      - Avoids storing all parsed rows as list[dict]
      - Uses list + join instead of repeated string concatenation
    """
    if not header_config:
        return ""

    header = _get_column_names(header_config)

    # Build header
    output_lines = []
    header_row = delimiter.join(f"{enclosed_by}{name}{enclosed_by}" for name in header)
    output_lines.append(header_row)

    # Process data line-by-line
    for raw_line in _get_line_iterator(raw_data_file):
        if not raw_line:  # skip empty lines
            continue

        parsed = _parse_data_by_line(
            header_config=header_config,
            raw_data_line=raw_line,
            trim_whitespace=trim_whitespace,
            offset=offset,
        )

        data_row = delimiter.join(
            f"{enclosed_by}{parsed[column]}{enclosed_by}" for column in header
        )
        output_lines.append(data_row)

    result = line_ending.join(output_lines)
    return result  # No need for final rstrip unless you specifically want to remove a trailing newline
