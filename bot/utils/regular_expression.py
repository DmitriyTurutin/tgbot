import re

def check_re(string: str) -> bool:
    match = re.match(r"\d{2}/\d{2}/\d{4}", string.strip())
    return match