import tomli


def get_configuration(config_file: str) -> dict:
    with open(config_file, "rb") as toml_config:
        config_dict = tomli.load(toml_config)
    return config_dict


def get_definitions(config_dict: dict) -> dict:
    if "definitions" not in config_dict:
        raise Exception("You are misisng the definitions section of your toml")
    config = config_dict["definitions"]
    return config


# TODO: Make sure to convert the list item from the config to a tuple of length 2
# TODO: Write some tests
