import i18n

from documents.user import User, DoesNotExist
from exceptions.userNotFound import UserNotFound
from validators.validateUserId import validate_user_id


def check_if_user_exists(_id, client, message):
    discord_user = client.get_user(_id)

    if discord_user is None:
        raise UserNotFound()

    try:
        user = User.objects.get(id=discord_user.id)
    except DoesNotExist:
        user = User(id=discord_user.id, name=discord_user.name)

    return user


def extract_user_id(string):
    validate_user_id(string)
    if string.startswith('<@!'):
        return int(string[3:-1])
    else:
        return int(string[2:-1])
