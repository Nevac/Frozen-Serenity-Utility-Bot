from validation import validate_text
from exceptions.userNotFound import UserNotFound
from validators.validateIntAsString import validate_int_as_string


def validate_user_id(key: str) -> int:
    if type(key) is int:
        return int(key)
    try:
        validate_text(key)

        if key.startswith('<@!') and key.endswith('>'):
            key = key[3:-1]
        elif key.startswith('<@') and key.endswith('>'):
            key = key[2:-1]
        elif key.isnumeric():
            pass
        else:
            raise ValueError()
        validate_int_as_string(key)
        return int(key)
    except Exception:
        raise UserNotFound
