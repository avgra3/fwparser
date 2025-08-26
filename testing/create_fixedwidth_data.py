"""Creating arbitrarily large fixed width datasets."""

from faker import Faker

Faker.seed(100)


class FixedWidthDataCreation:
    """Class to create fixed width data."""

    def __init__(
        self,
        definitions: dict[str, list[int, int]],
        delimiter: str = ",",
        generated_rows: int = 10,
        line_terminator: str = "\r\n",
    ) -> None:
        """definitions: dict[str, list[int, int]]: Column definitions with the
        field name (key) and a list with the starting character number and the
        length of the field.

        generated_rows: int: Number of rows you would like to generate.
        Defaults to 10.
        """
        self.customer_id = definitions["customer_id"]
        self.first_name = definitions["first_name"]
        self.last_name = definitions["last_name"]
        self.address = definitions["address"]
        self.phone_number = definitions["phone_number"]
        self.rows = generated_rows
        self.fake = Faker()
        self.delimiter = delimiter
        self.line_terminator = line_terminator

    def _customer_id(self) -> str:
        customer_id = (
            f"{self.fake.random_number(digits=self.customer_id[1], fix_len=True)}"
        )
        return customer_id.rjust(self.customer_id[1])

    def _first_name(self) -> str:
        return self.fake.first_name().rjust(self.first_name[1], " ")

    def _last_name(self) -> str:
        return self.fake.last_name().rjust(self.last_name[1], " ")

    def _address(self) -> str:
        return (self.fake.address().replace("\n", " ").replace(",", "")).rjust(
            self.address[1], " "
        )

    def _phone_number(self) -> str:
        phone_number = (
            f"{self.fake.random_number(digits=self.phone_number[1], fix_len=True)}"
        )
        return phone_number.rjust(self.phone_number[1], " ")

    def _fixed_width_and_delimited_line(self) -> dict[str, str]:
        customer_id = self._customer_id()
        first_name = self._first_name()
        last_name = self._last_name()
        address = self._address()
        phone_number = self._phone_number()
        fw = customer_id + first_name + last_name + address + phone_number
        delim = (
            customer_id
            + self.delimiter
            + first_name
            + self.delimiter
            + last_name
            + self.delimiter
            + address
            + self.delimiter
            + phone_number
        )
        return {
            "fixed_width": fw,
            "delimited": delim,
        }

    def generate_data_file(self) -> dict[str, str]:
        r"""Generates similated data.

        delimiter: str = \",\".
        """
        fixed_width = ""
        delimited = ""
        for row in range(self.rows):
            data = self._fixed_width_and_delimited_line()
            fixed_width += data["fixed_width"] + self.line_terminator
            delimited += data["delimited"] + self.line_terminator
        return {
            "fixed_width": fixed_width,
            "delimited": delimited,
        }
