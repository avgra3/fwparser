"""Convert parsed raw data to a Pandas dataframe."""

try:
    import pandas as pd
except ImportError as e:
    print(
        """Pandas does not appear to be installed which is required to output to
    a pandas dataframe."""
    )
    print("Either resintall using one of the optional paramerters => [pandas]")
    print(e)

from io import StringIO

from fwparser.fwparser import parse_data_file
from fwparser.toml_parser import toml_parse_data_file


def parse_to_pandas(
    raw_data_file: str,
    header_config: dict[str, tuple] | str,
    trim_white_space: bool = True,
    offset: int = 0,
    using_toml: bool = False,
    enclosed_by: str = "",
):
    """Parse raw data to a Pandas dataframe."""
    if isinstance(header_config, str) and using_toml:
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

    return pd.read_csv(
        StringIO(parsed_data),
        header=0,
        sep=",",
        quotechar=enclosed_by,
    )
