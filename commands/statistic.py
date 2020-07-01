import i18n

from util.utility import get_warnings_giver, get_warnings_taker, resolve_users


async def giver(message, client):
    await __top_stats(message, client, get_warnings_giver, 'dialogs.statistic.giver')


async def taker(message, client):
    await __top_stats(message, client, get_warnings_taker, 'dialogs.statistic.taker')


async def __top_stats(message, client, function, dialog_id: str):
    if not message.author.guild_permissions.administrator:
        return

    # TODO Cannot get it to work with mongoengine==0.8.8
    await message.channel.send('Ich bechume das mit excel nonid ane, google meint sum() aber mis excel verstaht keis englisch...')
    return

    command = message.content.split(' ')
    dialog = i18n.t(dialog_id)

    top = 5
    if len(command) == 3:
        if command[2].isnumeric():
            top = int(command[2])
        else:
            dialog = i18n.t('dialogs.statistic.invalid').format(command[2])

    top_warnings = function(top)
    dialog += '```' + '\n'.join([
        (str(k + 1) + '.').ljust(5) + ' '
        + str(w['warnings']).ljust(5) + ' '
        + resolve_users(client, str(w['_id']))
        for k, w in enumerate(top_warnings)]) + '```'

    await message.channel.send(dialog)
