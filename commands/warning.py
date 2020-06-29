from exceptions.commandIncomplete import CommandIncomplete
from exceptions.userNotFound import UserNotFound
from services.localizationService import i18n

from util.utility import extract_user_id, get_user, get_warnings, add_warning, get_warnings_top


async def warning(message, client):
    command = message.content.split(' ')

    try:
        validate_warning_user_argument(command)
        id_string = command[2]
        _id = extract_user_id(id_string)

        if _id == client.user.id:
            _id = message.author.id
            dialog = i18n.t('dialogs.warning.give_bot')
        elif _id == message.author.id:
            dialog = i18n.t('dialogs.warning.give_self')
        else:
            dialog = i18n.t('dialogs.warning.give')

        target = get_user(_id, client)
        author = get_user(message.author.id, client)
        add_warning(author, target, ' '.join(command[3:]))

        await message.channel.send(dialog.format(get_warnings(target)))
    except UserNotFound as e:
        await message.channel.send(e.message)
    except CommandIncomplete as e:
        await message.channel.send(e.message + '\n' + i18n.t('dialogs.error.command_incomplete'))


async def warnings(message, client):
    command = message.content.split(' ')

    try:
        user = get_user(message.author.id, client)
        top = int(command[2]) if len(command) == 3 and command[2].isnumeric() else 5
        if len(command) == 3 and not command[2].isnumeric():
            dialog = i18n.t('dialogs.warning.check_invalid').format(get_warnings(user), command[2])
        else:
            dialog = i18n.t('dialogs.warning.check').format(get_warnings(user))

        top_warnings = get_warnings_top(user, top)
        dialog += '```' + '\n'.join([
            w.date.strftime("%d.%m.%Y %H:%M:%S") + ' \t'
            + w.owner.name + ' \t'
            # TODO Resolve user IDs in reason
            + w.reason
            for w in top_warnings]) + '```'

        await message.channel.send(dialog)
    except UserNotFound as e:
        await message.channel.send(e.message)


def validate_warning_user_argument(command: list):
    if len(command) == 3:
        raise CommandIncomplete('{0} {1} {2} **{3}**'.format(command[0], command[1], command[2], i18n.t('dialogs.warning.missing_reason')))
    elif len(command) <= 2:
        raise CommandIncomplete('{0} {1} **@{2} {3}**'.format(command[0], command[1], i18n.t('dialogs.warning.missing_user'), i18n.t('dialogs.warning.missing_reason')))
