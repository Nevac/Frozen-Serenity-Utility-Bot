from exceptions.validationError import ValidationError


def validate_int_as_string(string):
    try:
        int(string)
    except Exception:
        raise ValidationError('Type of given value is not a string')
