BracesDict = dict[str, str ]
BracketDict = dict[str, str | BracesDict | None]

def parse_braces_dict(text: str, verbose: bool) -> BracesDict | None:
    if verbose:
        print(text)
    if not text.startswith("{"):
        return None
    result: BracesDict = {}
    is_open_braces = False
    is_in_quotes = False
    is_in_single_quotes = False
    is_escaped = False
    is_before_colon = True
    key: str = ""
    value: str = ""
    def accumulate(k: str, v: str, c: str) -> tuple[str, str]:
        if not is_in_quotes and not is_in_single_quotes:
            return k, v
        if is_before_colon:
            k += c
        else:
            v += c
        return k, v

    for character in text:
        if is_escaped:
            key, value = accumulate(key, value, character)
            is_escaped = False
            continue
        match character:
            case "{":
                is_open_braces = True
            case "}":
                is_open_braces = False
                break
            case ":":
                is_before_colon = False
                is_after_colon = True
            case ",":
                if len(key) > 0:
                    result[key] = value
                is_before_colon = True
                key = ""
                value = ""
            case "\"":
                if is_in_single_quotes:
                    key, value = accumulate(key, value, character)
                else:
                    is_in_quotes = not is_in_quotes
            case "\'":
                if is_in_quotes:
                    key, value = accumulate(key, value, character)
                    continue
                is_in_single_quotes = not is_in_single_quotes
            case "\\":
                is_escaped = True
            case _:
                key, value = accumulate(key, value, character)

    if len(key) > 0:
        result[key] = value

    if is_open_braces:
        print(f"Warning: braces not closed")

    if verbose:
        for key in result:
            print(f"{key}: {result[key]}")

    return result


def parse_bracket_dict(text: str) -> BracketDict:
    result: BracketDict = {}
    if not text.startswith("["):
        return result

    is_open_brackets = False
    is_open_brackets = False
    bracketed: str = ""
    content: str = ""
    for character in text:
        match character:
            case "[":
                if len(bracketed) > 0:
                    result[bracketed] = parse_braces_dict(content)
                bracketed = ""
                is_open_brackets = True
            case "]":
                content = ""
                is_open_brackets = False
            case _:
                if is_open_brackets:
                    bracketed += character
                else:
                    content += character
    if len(bracketed) > 0:
        result[bracketed] = parse_braces_dict(content)
    for key in result:
        print(f"{key}: {result[key]}")
    return result