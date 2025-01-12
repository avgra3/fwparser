from __future__ import annotations
from .fwparser import parse_data_file

IMPORTED = ("parse_data_file",)

try:
    from .toml_parser import toml_parse_data_file

    IMPORTED += ("toml_parse_data_file",)
except ImportError as e:
    pass

try:
    from .pandas import parse_to_pandas

    IMPORTED += ("parse_to_pandas",)
except ImportError as e:
    pass

try:
    from .polars import parse_to_polars

    IMPORTED += ("parse_to_polars",)
except ImportError as e:
    pass

# __all__ = ("parse_data_file",)
__all__ = IMPORTED
