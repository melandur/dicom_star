import re
import typing as t


def tokenize_filter_string(text: str) -> t.Optional[list]:
    """Tokenize a string into a filter string"""

    if isinstance(text, type(None)) or all(char.isspace() for char in text):
        return None

    text = re.sub(r'^[&|]+|[&|]+$', '', text)  # remove special characters at the beginning and end of the string
    text = text.strip()  # remove empty spaces at the beginning and end of the string

    text = re.sub(r'\s*&\s*', '&', text)  # remove empty spaces around the & symbol
    text = re.sub(r'\s*\|\s*', '|', text)  # remove empty spaces around the | symbol
    text = re.sub(r'\s*~\s*', '~', text)  # remove empty spaces around the ~ symbol
    text = re.sub(r'([&|~])\1+', r'\1', text)  # remove multiple consecutive special characters

    if bool(re.search(r'[&|][&|]', text)):  # & and | can not be neighbors
        return None

    if '~' in text:
        if not bool(re.search(r'(^~)|[&|]~', text)):  # ~ at start and after & or |
            return None

    if '&' in text or '|' in text:
        tokens = re.findall(r'(&|\||[^&|]+)', text)  # not & or | characters at the beginning and end of the string
    else:
        tokens = [text]

    return tokens


def create_filter_logic(tokens: list, search_type: str) -> t.Optional[str]:
    """Create a filter string from a list of filter tokens"""

    if tokens is None:
        return None

    filter_assembly = ''
    for token in tokens:
        if token == '&' or token == '|':
            filter_assembly += f' {token}'
        elif '~' in token:
            filter_assembly += f' ~{search_type}("{token[1:]}")'
        else:
            filter_assembly += f' {search_type}("{token}")'

    if filter_assembly != '':
        filter_assembly = f'({filter_assembly.lstrip()})'
    return filter_assembly
