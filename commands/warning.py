from services.localizationService import i18n

from util.utility import extractUserId
from documents.user import User, DoesNotExist


async def warning(message, client):
    command = message.content.split(' ')
    _id = int(extractUserId(command[2]))

    if _id == client.user.id:
        _id = message.author.id
        dialog = i18n.t('dialogs.warning.give_bot')
    elif _id == message.author.id:
        dialog = i18n.t('dialogs.warning.give_self')
    else:
        dialog = i18n.t('dialogs.warning.give')

    discord_user = client.get_user(_id)
    try:
        user = User.objects.get(id=discord_user.id)
    except DoesNotExist:
        user = User(id=discord_user.id, name=discord_user.name)

    user.warnings += 1
    user.save()

    await message.channel.send(dialog.format(user.warnings))


async def warnings(message, client):
    discord_user = client.get_user(message.author.id)
    try:
        user = User.objects.get(id=discord_user.id)
    except DoesNotExist:
        user = User(id=discord_user.id, name=discord_user.name)

    await message.channel.send(i18n.t('dialogs.warning.check').format(user.warnings))
