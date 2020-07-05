import i18n


async def none(message, client):
    await message.channel.send(i18n.t('dialogs.none'))


async def unknown(message, client):
    await message.channel.send(i18n.t('dialogs.error.command_not_found').format(i18n.t('commands.help')))
