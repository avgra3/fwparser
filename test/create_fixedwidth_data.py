from faker import Faker

Faker.seed(100)


class FixedWidthDataCreation:
    def __init__(
        self, definitions: dict[str, list[int, int]], generated_rows: int = 10
    ) -> None:
        self.customer_id = definitions["customer_id"]
        self.first_name = definitions["first_name"]
        self.last_name = definitions["last_name"]
        self.address = definitions["address"]
        self.phone_number = definitions["phone_number"]
        self.rows = generated_rows
        self.fake = Faker()

    def _customer_id(self) -> str:
        return f"{self.fake.random_number(digits=self.customer_id[1], fix_len=True)}".rjust(
            self.customer_id[1]
        )

    def _first_name(self) -> str:
        return self.fake.first_name().rjust(self.first_name[1], " ")

    def _last_name(self) -> str:
        return self.fake.last_name().rjust(self.last_name[1], " ")

    def _address(self) -> str:
        return (self.fake.address().replace("\n", " ").replace(",", "")).rjust(
            self.address[1], " "
        )

    def _phone_number(self) -> str:
        return f"{self.fake.random_number(digits=self.phone_number[1], fix_len=True)}".rjust(
            self.phone_number[1], " "
        )

    def _fixed_width_and_delimited_line(self, delimiter=",") -> dict[str, str]:
        customer_id = self._customer_id()
        first_name = self._first_name()
        last_name = self._last_name()
        address = self._address()
        phone_number = self._phone_number()
        return {
            "fixed_width": customer_id
            + first_name
            + last_name
            + address
            + phone_number,
            "delimited": customer_id
            + delimiter
            + first_name
            + delimiter
            + last_name
            + delimiter
            + address
            + delimiter
            + phone_number,
        }

    def generate_data_file(self, delimiter: str = ",") -> dict[str, str]:
        delimited = ""
        fixed_width = ""
        for row in range(self.rows):
            data = self._fixed_width_and_delimited_line(delimiter=delimiter)
            delimited += data["fixed_width"] + "\r\n"
            fixed_width += data["delimited"] + "\r\n"
        return {"fixed_width": fixed_width, "delimited": delimited}
