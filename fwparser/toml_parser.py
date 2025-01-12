import tomli
import os
from fwparser.fwparser import parse_data_file


def _get_configuration(config_file: str) -> dict:
    if (
        os.path.isfile(config_file)
        and os.path.split(config_file)[1].split(".")[-1].lower() == "toml"
    ):
        with open(config_file, "rb") as toml_config:
            config_dict = tomli.load(toml_config)
        return config_dict
    raise Exception(
        f'The configuration file: {config_file} is not a file or does not have the "toml" extension'
    )


def _get_definitions(config_dict: dict) -> dict:
    if "definitions" not in config_dict:
        raise Exception("You are misisng the definitions section of your toml")
    config = config_dict["definitions"]
    return config


def _turn_lists_to_tuples(config: dict[list]) -> dict[tuple]:
    correct_config = {}
    for key in config:
        correct_config[key] = (config[key][0], config[key][1])
    return correct_config


def toml_parse_data_file(
    raw_data_file: str,
    toml_file_path: str,
    trim_whitespace: bool = False,
    offset: int = 0,
) -> str:
    toml_file = _turn_lists_to_tuples(
        _get_definitions(config_dict=_get_configuration(config_file=toml_file_path))
    )
    return parse_data_file(
        raw_data_file=raw_data_file,
        header_config=toml_file,
        trim_whitespace=trim_whitespace,
        offset=offset,
    )
