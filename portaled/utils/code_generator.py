import random
import string


def generate_random_code(length: int = 10, prefix: str | None = None) -> str:
    """Generate a random code containing uppercase letters and digits.
    The default length of the random code is 10.
    """
    # Define the pool of characters to choose from
    characters = string.ascii_uppercase + string.digits

    # Generate the random code
    random_code = "".join(random.choices(characters, k=length))

    if prefix:
        random_code = f"{prefix}_{random_code}"
    return random_code
