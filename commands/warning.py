from exceptions.commandIncomplete import CommandIncomplete
from exceptions.userNotFound import UserNotFound
from services.localizationService import i18n

from util.utility import get_user, is_user, add_warning, get_warnings, get_warnings_top
from validators.validateUserId import validate_user_id


async def warning(message, client):
    command = message.content.split(' ')

    try:
        validate_warning_user_argument(command)
        target_id = validate_user_id(command[2])
        owner_id = message.author.id

        if target_id == client.user.id:
            target_id = message.author.id
            owner_id = client.user.id
            dialog = i18n.t('dialogs.warning.give_bot')
        elif target_id == message.author.id:
            dialog = i18n.t('dialogs.warning.give_self')
        else:
            dialog = i18n.t('dialogs.warning.give')

        target = get_user(client, target_id)
        author = get_user(client, owner_id)
        add_warning(author, target, ' '.join(command[3:]).strip())

        await message.channel.send(dialog.format(get_warnings(target)))
    except UserNotFound as e:
        await message.channel.send(e.message)
    except CommandIncomplete as e:
        await message.channel.send(e.message + '\n' + i18n.t('dialogs.error.command_incomplete'))


async def warnings(message, client):
    command = message.content.split(' ')

    try:
        user = get_user(client, message.author.id)

        dialog = i18n.t('dialogs.warning.check').format(get_warnings(user))
        if len(command) == 3:
            if not command[2].isnumeric():
                dialog = i18n.t('dialogs.warning.check_invalid').format(get_warnings(user), command[2])
            else:
                top = int(command[2])
                top_warnings = get_warnings_top(user, top)
                dialog += '```' + '\n'.join([
                    w.date.strftime("%d.%m.%Y %H:%M:%S") + ' '
                    + w.owner.name.ljust(25) + ' '
                    + __resolve_users(client, w.reason)
                    for w in top_warnings]) + '```'

        await message.channel.send(dialog)
    except UserNotFound as e:
        await message.channel.send(e.message)


def __resolve_users(client, words: str):
    return ' '.join(['@' + user.name if (user := is_user(client, w)) is not None else w for w in words.split(' ')])


def validate_warning_user_argument(command: list):
    if len(command) == 3:
        raise CommandIncomplete('{0} {1} {2} **{3}**'.format(command[0], command[1], command[2], i18n.t('dialogs.warning.missing_reason')))
    elif len(command) <= 2:
        raise CommandIncomplete('{0} {1} **@{2} {3}**'.format(command[0], command[1], i18n.t('dialogs.warning.missing_user'), i18n.t('dialogs.warning.missing_reason')))
