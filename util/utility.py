from datetime import datetime

from discord import Client
from mongoengine import DoesNotExist

from documents.warnig import Warnig
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


def __get_username(client: Client, key: str) -> User or str:
    try:
        return get_user(client, key).name
    except UserNotFound as e:
        return key


def resolve_users(client, words: str):
    return ' '.join(['@' + __get_username(client, w) for w in words.split(' ')])


def add_warning(giver: User, taker: User, reason: str) -> None:
    reason = Warnig(date=datetime.now, giver=giver, taker=taker, reason=reason)
    reason.save()


def get_warnings(user: User) -> int:
    # TODO Backwards compatibility, should old warnings still be counted?
    return Warnig.objects.filter(taker=user).count() + user.warnings


def get_warnings_top(user: User, top: int = 5):
    return Warnig.objects.filter(taker=user).order_by('-date')[:top]


def get_warnings_giver(top: int = 5):
    warnings_giver = Warnig.objects.aggregate([{'$group': {'_id': '$giver', 'warnings': {'$sum': 1}}}, {'$sort': {'warnings': -1}}])
    return list(warnings_giver)[:top]


def get_warnings_taker(top: int = 5):
    warnings_taker = Warnig.objects.aggregate([{'$group': {'_id': '$taker', 'warnings': {'$sum': 1}}}, {'$sort': {'warnings': -1}}])
    return list(warnings_taker)[:top]
