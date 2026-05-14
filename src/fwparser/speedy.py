import os
from collections.abc import Generator, Iterator
from itertools import islice
from multiprocessing import Process, Queue
from pathlib import Path

from .errors import IndexOutOfBoundsError, NotAFile, NotEnoughCpus


class FastFwparser:
    def __init__(
        self,
        data: str | Path,
        header_config: dict[str, tuple[int, int]],
        trim_whitespace: bool = False,
        offset: int = 0,
        enclosed_by: str = "",
        sep: str = ",",
        line_ending: str = "\r\n",
        max_cpu: int = 1,
        chunk_size: int = 50_000,
    ) -> None:
        self.data_source = data
        self.is_file = isinstance(data, Path)

        if self.is_file:
            path = Path(data)
            if not path.is_file():
                raise NotAFile(f"`{path}` is not a valid file")
            self.file_path = path
        else:
            self.file_path = None
            self.raw_data = data

        self.header_config = header_config
        self.trim_whitesplace = trim_whitespace
        self.offset = offset
        self.cpus = min(max_cpu, os.cpu_count() or 1)
        self.enclosed_by = enclosed_by
        self.sep = sep
        self.line_ending = line_ending
        self.header_names: list[str] = []
        self.parsed_header = ""
        self.chunk_size = chunk_size
        if self.cpus < 1:
            raise NotEnoughCpus("Cpus < 1.")

    def _get_column_names(self):
        header_order = [(name, pos) for name, (pos, _) in self.header_config.items()]
        header_order.sort(key=lambda x: x[1])
        self.header_names = [name for name, _ in header_order]

    def _parse_data_by_line(self, raw_data_line: str) -> dict[str, str]:
        parsed_field = {}
        for value in self.header_config.items():
            header = value[0]
            value_start = int(value[1][0]) - self.offset
            if value_start < 0:
                raise IndexOutOfBoundsError(
                    message="Index out of bounds", field_name=header
                )
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
        quoted = f"{self.enclosed_by}{{}}{self.enclosed_by}"
        self.parsed_header = (
            self.sep.join(quoted.format(name) for name in self.header_names)
            + self.line_ending
        )

    def _parse_line(self, line: str) -> dict[str, str]:
        parsed: dict[str, str] = {}
        for header, (start, length) in self.header_config.items():
            start_index = int(start) - self.offset
            if start_index < 0:
                raise IndexOutOfBoundsError(
                    field_name=header, message="Index out of bounds"
                )
            end_index = start_index + int(length)
            value = line[start_index:end_index]
            parsed[header] = value.strip() if self.trim_whitesplace else value
        return parsed

    def _lines_iter(self) -> Iterator[str]:
        if not self.is_file and isinstance(self.raw_data, str):
            yield from self.raw_data.split(self.line_ending)
            return
        if self.file_path is None:
            raise TypeError("File path should be of type Path NOT None")
        with open(self.file_path, encoding="utf-8", errors="replace") as f:
            yield from f

    def _chunked_lines(self) -> Generator[list[str], None, None]:
        item = self._lines_iter()
        while True:
            chunk = list(islice(item, self.chunk_size))
            if not chunk:
                break
            yield chunk

    def _data_list_to_csv(self, data_list: list[dict[str, str]]) -> str:
        if not data_list:
            return ""
        lines = []
        quoted = f"{self.enclosed_by}{{}}{self.enclosed_by}"
        for row in data_list:
            line = self.sep.join(quoted.format(row[col]) for col in self.header_names)
            lines.append(line + self.line_ending)
        return "".join(lines).rstrip(self.line_ending)

    def _producer(self, q: Queue, data: list[str]) -> None:
        try:
            parsed_chunk = [
                self._parse_line(line.rstrip(self.line_ending))
                for line in data
                if line != ""
            ]
            csv_chunk = self._data_list_to_csv(parsed_chunk)
            q.put(csv_chunk)
        except Exception as e:
            q.put(e)

    def _consumer(self, q: Queue, number_of_parts: int) -> str:
        result_parts = []
        for _ in range(number_of_parts):
            item = q.get()
            if isinstance(item, Exception):
                raise item
            result_parts.append(item)
        return "".join(result_parts)

    def parse_data_file(self) -> str:
        self._get_column_names()
        self._get_header_line()

        if self.cpus <= 1:
            result = []
            for chunk in self._chunked_lines():
                parsed = [
                    self._parse_line(line.rstrip(self.line_ending)) for line in chunk
                ]
                result.append(self._data_list_to_csv(parsed))
            body = "".join(result)
            return self.parsed_header + body.rstrip(self.line_ending)

        mp = []
        q: Queue = Queue()
        count = 0
        for chunk in self._chunked_lines():
            p = Process(target=self._producer, args=(q, chunk))
            p.start()
            mp.append(p)
            count += 1

        try:
            body = self._consumer(q, count)
        finally:
            for p in mp:
                p.join()

        return self.parsed_header + body

        # .rstrip(self.line_ending).rstrip(
        #    self.sep * len(self.header_names)
        # )
