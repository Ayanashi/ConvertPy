import re


def sanitize_filename(filename: str) -> str:
    return re.sub(r"[^\w\-_\. ]", "_", filename)
