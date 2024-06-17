from pydantic import SecretStr


class SecretField(SecretStr):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        # Add custom validation logic for password strength here
        return str(v)

    def __repr__(self):
        return "*" * len(self)  # Hide value in string representation
