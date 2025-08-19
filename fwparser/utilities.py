"""Utilities for fwparser."""

from errors import NoLineTerminatorError


def get_line_terminator(filename: str):
    """Creates line terminator. Default is '\\r\\n'."""
    with open(filename, "rb") as f:
        first_line = f.readline()
        if b"\r\n" in first_line:
            return "\r\n"
        if b"\n" in first_line:
            return "\n"
        return None


def split_data_by_line(
    raw_data: str,
    line_terminator: str = None,
) -> list[str]:
    """Split raw data into lines.

    raw_data: str
    line_terminator: str = None
    return list[str]
    """
    if line_terminator is None:
        raise NoLineTerminatorError()
    data = raw_data.split(line_terminator)
    return data
