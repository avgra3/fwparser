__all__ = [
    "fwparser.fwparser.parse_data_file",
    "fwparser.errors.NoLineTerminatorError",
]
try:
    import tomli

    del tomli
    __all__.append("fwparser.toml_parser.toml_parse_data_file")
except ImportError:
    pass
try:
    import pandas

    del pandas

    __all__.append("fwparser.pandas.parse_to_pandas")
except ImportError:
    pass
try:
    import polars

    del polars
    __all__.append("fwparser.polars.parse_to_polars")
except ImportError:
    pass
