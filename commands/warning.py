from exceptions.commandIncomplete import CommandIncomplete
from exceptions.userNotFound import UserNotFound
from services.localizationService import i18n

from util.utility import get_user, resolve_users, add_warning, get_warnings, get_warnings_top
from validators.validateUserId import validate_user_id


async def warning(message, client):
    command = message.content.split(' ')

    try:
        validate_warning_user_argument(command)
        taker_id = validate_user_id(command[2])
        giver_id = message.author.id

        if taker_id == client.user.id:
            taker_id = message.author.id
            giver_id = client.user.id
            dialog = i18n.t('dialogs.warning.give_bot')
        elif taker_id == message.author.id:
            dialog = i18n.t('dialogs.warning.give_self')
        else:
            dialog = i18n.t('dialogs.warning.give')

        giver = get_user(client, giver_id)
        taker = get_user(client, taker_id)
        add_warning(giver, taker, ' '.join(command[3:]).strip())

        await message.channel.send(dialog.format(get_warnings(taker)))
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
                top_warnings = get_warnings_top(user, int(command[2]))
                dialog += '```' + '\n'.join([
                    w.date.strftime("%d.%m.%Y %H:%M:%S") + ' '
                    + w.giver.name.ljust(25) + ' '
                    + resolve_users(client, w.reason)
                    for w in top_warnings]) + '```'

        await message.channel.send(dialog)
    except UserNotFound as e:
        await message.channel.send(e.message)


def validate_warning_user_argument(command: list):
    if len(command) == 3:
        raise CommandIncomplete('{0} {1} {2} **{3}**'.format(command[0], command[1], command[2], i18n.t('dialogs.warning.missing_reason')))
    elif len(command) <= 2:
        raise CommandIncomplete('{0} {1} **@{2} {3}**'.format(command[0], command[1], i18n.t('dialogs.warning.missing_user'), i18n.t('dialogs.warning.missing_reason')))
