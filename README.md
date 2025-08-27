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
from fwparser.fwparser import parse_data_file

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

### Multiprocessing

If you have a large file, think 1 million lines and/or 100+ fields of data, you should consider using the multiprocessing module.

There are some things to note before running this method:

- Do you have a low core count available to you? (Less than 2). If so, this method may actually take longer than the single threaded version because of the overhead of orchestrating the threads.

- Do you have a large enough file for this to make sense? Is your file large in row count and/or field counts? This would be like having a around 1 million+ lines and/or around 50+ fields.

Here is an example:

```python
from fwparser.speedy import FastFwparser

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

TRIM_WHITESPACE = True
OFFSET = 1
ENCLOSED_BY = ""
SEP = ","
LINE_ENDING = "\r\n"
MAX_CPUS = 4

fwparser_object = FastFwparser(
        data=FIXED_WIDTH_FILE,
        header_config=DATA_OUTLINE,
        trim_whitespace=TRIM_WHITESPACE,
        offset=OFFSET,
        enclosed_by=ENCLOSED_BY,
        sep=SEP,
        line_ending=LINE_ENDING,
        max_cpu = MAX_CPUS,
)

data = fwparser_object.parse_data_file()

print(data)

"""
customer_id,first_name,last_name,address,phone_number
12345,John,Doe,123 Main St,1234567890
"""
```

### Optional Dependencies

You can optionally install the package to have [Toml](https://toml.io/en/), [Pandas](https://duckduckgo.com/?t=ffab&q=python+pandas), or [Polars](https://pola.rs/) support.

```bash
# With Toml support
pip install --upgrade "fwparser[toml] @ git+https://github.com/avgra3/fwparser.git"

# With Pandas support -- includes toml support
pip install --upgrade "fwparser[pandas] @ git+https://github.com/avgra3/fwparser.git"

# With Polars support -- includes toml support
pip install --upgrade "fwparser[polars] @ git+https://github.com/avgra3/fwparser.git"

# With Polars, Pandas, and Toml support
pip install --upgrade "fwparser[all] @ git+https://github.com/avgra3/fwparser.git"
```

## Why

You might be wondering why this package exists. Simply, I found that the pandas and polars implementations for parsing file types like these were clunky and not the main focus of those projects.

As the method currently works, you can easily move to working with a pandas or polars dataframe from the data here.

The base implementation of this project does not use any external dependencies. As long as you have a Python version >=3.8, this project should work for your needs.

## Issues/Bugs

If you find any issues while using this module feel free to open an issue or open a pull request for any bug fixes you find.

## Benchmarking

From the project source directory, run the command `make benchmark`. The benchmark will run and all results will be output into [Benchmark_Results](Benchmark_Results/) directory.

Making the test file will take a while to make. If you have already ran the benchmark, the creation of the file will be skipped.
