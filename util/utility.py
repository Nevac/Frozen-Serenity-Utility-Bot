from datetime import datetime

from mongoengine import DoesNotExist

from documents.reason import Reason
from documents.user import User
from exceptions.userNotFound import UserNotFound
from validators.validateUserId import validate_user_id


def get_user(_id, client):
    discord_user = client.get_user(_id)

    if discord_user is None:
        raise UserNotFound()

    try:
        user = User.objects.get(id=discord_user.id)
    except DoesNotExist:
        user = User(id=discord_user.id, name=discord_user.name)
        user.save()

    return user


def extract_user_id(string: str) -> int:
    validate_user_id(string)
    if string.startswith('<@!'):
        return int(string[3:-1])
    else:
        return int(string[2:-1])


def add_warning(owner: User, target: User, reason: str):
    reason = Reason(date=datetime.now, owner=owner, target=target, reason=reason)
    reason.save()


def get_warnings(user: User):
    # TODO Backwards compatibility, should old warnings still be counted?
    return Reason.objects.filter(target=user).count() + user.warnings


def get_warnings_top(user: User, top: int = 5):
    return Reason.objects.filter(target=user).order_by('-date')[:top]
