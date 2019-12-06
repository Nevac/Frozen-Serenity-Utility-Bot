from exceptions.commandIncomplete import CommandIncomplete
from exceptions.userNotFound import UserNotFound
from services.localizationService import i18n
from validation import validate_int

from util.utility import extract_user_id, check_if_user_exists
from documents.user import User, DoesNotExist
from validators.validateUserId import validate_user_id


async def warning(message, client):
    command = message.content.split(' ')

    try:
        validate_warning_user_argument(command)
        id_string = command[2]
        _id = extract_user_id(id_string)

        user = check_if_user_exists(_id, client, message)
        user.warnings += 1
        user.save()

        if _id == client.user.id:
            _id = message.author.id
            dialog = i18n.t('dialogs.warning.give_bot')
        elif _id == message.author.id:
            dialog = i18n.t('dialogs.warning.give_self')
        else:
            dialog = i18n.t('dialogs.warning.give')

        await message.channel.send(dialog.format(user.warnings))
    except UserNotFound as e:
        await message.channel.send(e.message)
    except CommandIncomplete as e:
        await message.channel.send(e.message + '\n' + i18n.t('dialogs.error.command_incomplete'))


async def warnings(message, client):
    try:
        user = check_if_user_exists(message.author.id, client, message)
        await message.channel.send(i18n.t('dialogs.warning.check').format(user.warnings))
    except UserNotFound as e:
        await message.channel.send(e.message)


def validate_warning_user_argument(command):
    if len(command) < 3:
        raise CommandIncomplete('{0} {1} **@UserX**'.format(command[0], command[1]))
