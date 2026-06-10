def get_within_curly_braces(text: str) -> str:
    found_first_brace = False
    levels = 0
    result: str = ""
    for character in text:
        if found_first_brace:
            result += character
            match character:
                case "{":
                    levels += 1
                case "}":
                    levels -= 1
            if levels == 0:
                return result
            continue
        if character != "{":
            continue
        found_first_brace = True
        levels += 1
        result += character
    if levels == 0:
        return result

    raise Exception(f"Curly braces level not matched on end: {levels}")