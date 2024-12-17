class NoLineTerminatorError(Exception):
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        base_message = "You must include a line terminator"
        if self.error_code:
            return f"{base_message}\n{self.args[0]} (Error code: {self.error_code})"
        return f"{base_message}\n{self.args[0]}"

class IndexOutOfBoundsError(Exception):
    def __init__(self, field_name, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code
        self.field_name = field_name

    def __str__(self):
        base_message = f"Start index of field name \"{self.field_name}\" is less than zero. Confirm your offset value and your configuration."
        return f"{base_message}\n{self.args[0]}"
