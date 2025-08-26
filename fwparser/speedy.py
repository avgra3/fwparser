from pathlib import Path
from multiprocessing import Process, Queue
from .errors import IndexOutOfBoundsError, NotAFile, NotEnoughCpus
import os
from itertools import islice


class FastFwparser:
    def __init__(
        self,
        data: str | Path,
        header_config: dict[str, tuple],
        trim_whitespace: bool = False,
        offset: int = 0,
        enclosed_by: str = "",
        sep: str = ",",
        line_ending: str = "\r\n",
        max_cpu: int = 1,
    ) -> None:
        if isinstance(data, Path):
            if not os.path.isfile(data):
                raise NotAFile()
            with open(data) as file:
                self.data = file.read().splitlines()
        else:
            self.data = data.splitlines()
        self.header_names = []
        self.header_config = header_config
        self.trim_whitesplace = trim_whitespace
        self.offset = offset
        self.result_list = []
        self.cpus = max_cpu if os.cpu_count() >= max_cpu else 1
        self.parsed = ""
        self.enclosed_by = enclosed_by
        self.sep = sep
        self.line_ending = line_ending

        if self.cpus == 1:
            raise NotEnoughCpus("Cpus <= 2")

    def _get_column_names(self):
        header_order = []
        for key in self.header_config:
            header_order.append((key, self.header_config[key][0]))
        _sorted = sorted(header_order, key=lambda x: x[1])
        result = []
        for i in range(len(_sorted)):
            result.append(_sorted[i][0])
        self.header_names = result

    def _parse_data_by_line(self, raw_data_line: str) -> dict[str, str]:
        parsed_field = {}
        for value in self.header_config.items():
            header = value[0]
            value_start = int(value[1][0]) - self.offset
            if value_start < 0:
                raise IndexOutOfBoundsError(field_name=header)
            value_end = value_start + int(value[1][1])
            data = raw_data_line[value_start:value_end]
            if self.trim_whitesplace:
                parsed_field[header] = data.strip()
            else:
                parsed_field[header] = data
        return parsed_field

    def _parse_all_data(self, data: list[str]) -> list[dict[str, str]]:
        result = []
        for line in data:
            row_data = self._parse_data_by_line(raw_data_line=line)
            result.append(row_data)
        return result

    def _get_header_line(self) -> None:
        for name in self.header_names:
            self.parsed += f"{self.enclosed_by}{name}{self.enclosed_by}{self.sep}"
        self.parsed = self.parsed.rstrip(self.sep) + self.line_ending

    def _chunk_data(self):
        chunk_size = len(self.data) // self.cpus
        it = iter(self.data)
        while True:
            chunk = list(islice(it, chunk_size))
            if not chunk:
                break
            yield chunk

    def _data_list_to_line(self, data_list: dict[str, str]) -> str:
        result = ""
        for line in data_list:
            data = ""
            for column in self.header_names:
                data += self.enclosed_by + line[column] + self.enclosed_by + self.sep
            result += data.rstrip(self.sep) + self.line_ending
        return result

    def _producer(self, q: Queue, data: list[str]) -> None:
        data_list = self._parse_all_data(data=data)
        lines = self._data_list_to_line(data_list=data_list)
        q.put(lines)

    def _consumer(self, q: Queue, number_of_parts: int) -> str:
        final_string = ""
        for _ in range(number_of_parts):
            final_string += q.get()
        return final_string

    def parse_data_file(self) -> str:
        self._get_column_names()
        self._get_header_line()
        mp = []
        q = Queue()
        count = 0
        for chunk in self._chunk_data():
            p = Process(target=self._producer, args=(q, chunk))
            p.start()
            mp.append(p)
            count += 1

        final_result = self._consumer(q, count)
        for p in mp:
            p.join()
        return self.parsed + final_result.rstrip(self.line_ending)
