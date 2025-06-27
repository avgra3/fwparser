from .errors import IndexOutOfBoundsError
import os


def _get_column_names(header_config: dict[str, tuple]) -> list[str]:
    header_order = []
    for key in header_config:
        header_order.append((key, header_config[key][0]))
    _sorted = sorted(header_order, key=lambda x: x[1])
    result = []
    for i in range(len(_sorted)):
        result.append(_sorted[i][0])
    return result


def _parse_data_by_line(
    header_config: dict[str, tuple],
    raw_data_line: str,
    trim_whitespace: bool = False,
    offset: int = 0,
) -> dict[str, str]:
    parsed_field = {}
    for value in header_config.items():
        header = value[0]
        value_start = int(value[1][0]) - offset
        if value_start < 0:
            raise IndexOutOfBoundsError(field_name=header)
        value_end = value_start + int(value[1][1])
        data = raw_data_line[value_start:value_end]
        if trim_whitespace:
            parsed_field[header] = data.strip()
        else:
            parsed_field[header] = data
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
        with open(raw_data_file, "r") as file:
            data = file.read().splitlines()
        return data
    if os.path.isdir(raw_data_file):
        raise Exception(f'The filepath, "{raw_data_file}", you put is a directory...')
    if isinstance(raw_data_file, str):
        data = raw_data_file.splitlines()
        return data
    raise Exception(
        f"The raw data path you included is not a file path or of type string:\n{raw_data_file}"
    )


def parse_data_file(
    raw_data_file: str,
    header_config: dict[str, tuple],
    trim_whitespace: bool = False,
    offset: int = 0,
    enclosed_by: str = ""
) -> str:
    header = _get_column_names(header_config=header_config)
    raw_data_list = _split_data(raw_data_file=raw_data_file)
    data_list = _parse_all_data(
        all_data=raw_data_list,
        header_config=header_config,
        trim_whitespace=trim_whitespace,
        offset=offset,
    )
    result = ""
    for name in header:
        result += f"{enclosed_by}{name}{enclosed_by},"
    result = result.rstrip(",") + "\r\n"

    for line in data_list:
        data = ""
        for column in header:
            data += enclosed_by + line[column] + enclosed_by + ","
        result += data.rstrip(",") + "\r\n"

    return result
