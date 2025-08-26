"""Constants sued throughout testing."""

VALID_TEST_TOML = "./testing/tests/test_valid_toml.toml"
INVALID_TEST_TOMLS = [
    "./testing/tests/test_invalid_toml.toml",
    "INVALID_TEST",
    "NOT_TOML",
]

RAW_DATA = "12345John      Doe       123 Main St         1234567890"
DATA_OUTLINE = {
    "customer_id": (0, 5),
    "first_name": (5, 10),
    "last_name": (15, 10),
    "address": (25, 20),
    "phone_number": (45, 10),
}
