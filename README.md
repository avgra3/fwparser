# FWParser

A simple parser for fixed width files.

## Installation

There are no dependencies required to use this module. Simply run:

```bash
pip install --upgrade git+https://github.com/avgra3/fwparser.git
```

Or

```bash
git clone https://github.com/avgra3/fwparser.git
cd ./fwparser
python -m pip install .
```

## Usage

Once you have fwparser installed, you can use it like below:

```python
from fwparser import parse_data_file

"""
# Assuming foo.txt contains the below
12345John      Doe       123 Main St         1234567890
"""
FIXED_WIDTH_FILE = "foo.txt"

# Needed in order to parse
DATA_OUTLINE = {
    "customer_id": (1, 5),
    "first_name": (6, 10),
    "last_name": (16, 10),
    "address": (26, 20),
    "phone_number": (46, 10),
}


data = parse_data_file(
        raw_data_file=FIXED_WIDTH_FILE,
        header_config=DATA_OUTLINE,
        trim_white_space=True, # This makes the result cleaner
        offset=1, # Only use if your config does not have an index at zero
)

print(data)
"""
customer_id,first_name,last_name,address,phone_number
12345,John,Doe,123 Main St, 1234567890
"""
```

With the above, you can then either save the data to a file or use another package like [pandas](https://pandas.pydata.org/) or [polars](https://pola.rs/) to work more with the data.

## Why

You might be wondering why this package exists. Simply, I found that the pandas and polars implementations for parsing file types like these were clunky and not the main focus of those projects.

As the method currently works, you can easily move to working with a pandas or polars dataframe from the data here.

The base implementation of this project does not use any external dependencies. As long as you have a Python version >=3.8, this project should work for your needs.

## Issues/Bugs

If you find any issues while using this module feel free to open an issue or open a pull request for any bug fixes you find.
