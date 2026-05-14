"""Utility to parse and convert to Polars dataframe."""

try:
    import polars as pl
except ImportError as e:
    print(
        """Polars does not appear to be installed which is required to output
        to a polars dataframe.
    Either resintall using one of the optional paramerters => [polars]
    or install polars directly"""
    )

    print(e)

from io import StringIO

from fwparser.fwparser import parse_data_file
from fwparser.toml_parser import toml_parse_data_file


def parse_to_polars(
    raw_data_file: str,
    header_config: str | dict[str, tuple[int, int]],
    trim_white_space: bool = True,
    offset: int = 0,
    using_toml: bool = False,
    enclosed_by: str = "",
):
    """Parse raw data to Polars dataframe."""
    if using_toml and isinstance(header_config, str):
        parsed_data = toml_parse_data_file(
            raw_data_file=raw_data_file,
            toml_file_path=header_config,
            trim_whitespace=trim_white_space,
            offset=offset,
            enclosed_by=enclosed_by,
        )
    elif (
        isinstance(header_config, dict)
        and all(isinstance(item, str) for item in header_config)
        and all(isinstance(header_config[item], tuple) for item in header_config)
        and all(len(header_config[item]) == 2 for item in header_config)
    ):
        parsed_data = parse_data_file(
            raw_data_file=raw_data_file,
            header_config=header_config,
            trim_whitespace=trim_white_space,
            offset=offset,
            enclosed_by=enclosed_by,
        )

    return pl.read_csv(
        StringIO(parsed_data),
        has_header=True,
        separator=",",
        infer_schema=False,
        quote_char=enclosed_by,
    )
