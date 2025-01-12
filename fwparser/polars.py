try:
    import polars as pl
except ImportError as e:
    print(
        """Polars does not appear to be installed which is required to output to a pandas dataframe.
    Either resintall using one of the optional paramerters => [polars]
    or install polars directly"""
    )

    print(e)

from io import StringIO
from fwparser.fwparser import parse_data_file
from fwparser.toml_parser import toml_parse_data_file


def parse_to_polars(
    raw_data_file: str,
    header_config: dict[str, tuple] | str,
    trim_white_space: bool = True,
    offset: int = 0,
    using_toml: bool = False,
):
    if using_toml:
        parsed_data = toml_parse_data_file(
            raw_data_file=raw_data_file,
            toml_file_path=header_config,
            trim_whitespace=trim_white_space,
            offset=offset,
        )
    else:
        parsed_data = parse_data_file(
            raw_data_file=raw_data_file,
            header_config=header_config,
            trim_whitespace=trim_white_space,
            offset=offset,
        )

    return pl.read_csv(
        StringIO(parsed_data), has_header=True, separator=",", infer_schema=False
    )
