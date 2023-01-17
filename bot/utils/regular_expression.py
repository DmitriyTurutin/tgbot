import re


def check_re(string: str) -> bool:
    match = re.match(r"^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/\d{4}$", string.strip())
    return match is not None
