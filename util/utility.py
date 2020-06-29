from datetime import datetime

from discord import Client
from mongoengine import DoesNotExist

from documents.reason import Reason
from documents.user import User
from exceptions.userNotFound import UserNotFound
from validators.validateUserId import validate_user_id


def get_user(client: Client, _id: str) -> User:
    user_id = validate_user_id(_id)
    discord_user = client.get_user(user_id)
    if discord_user is None:
        raise UserNotFound()

    try:
        user = User.objects.get(id=discord_user.id)
    except DoesNotExist:
        user = User(id=discord_user.id, name=discord_user.name)
        user.save()

    return user


def is_user(client, key: str) -> User or None:
    try:
        return get_user(client, key)
    except UserNotFound as e:
        return None


def add_warning(owner: User, target: User, reason: str) -> None:
    reason = Reason(date=datetime.now, owner=owner, target=target, reason=reason)
    reason.save()


def get_warnings(user: User) -> int:
    # TODO Backwards compatibility, should old warnings still be counted?
    return Reason.objects.filter(target=user).count() + user.warnings


def get_warnings_top(user: User, top: int = 5):
    return Reason.objects.filter(target=user).order_by('-date')[:top]
