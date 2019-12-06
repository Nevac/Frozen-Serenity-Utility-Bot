from validation import validate_text
from exceptions.userNotFound import UserNotFound
from validators.validateIntAsString import validate_int_as_string


def validate_user_id(string):
    try:
        validate_text(string)

        if string.startswith('<@!') and string.endswith('>'):
            string = string[3:-1]
        elif string.startswith('<@') and string.endswith('>'):
            string = string[2:-1]
        else:
            raise ValueError()
        validate_int_as_string(string)
    except Exception:
        raise UserNotFound
