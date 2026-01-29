import re

URL_REGEX = re.compile(
    r'^(https?:\/\/)'
    r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'
    r'(\/\S*)?$'
)

def is_valid_url(url: str) -> bool:
    return bool(URL_REGEX.match(url))
