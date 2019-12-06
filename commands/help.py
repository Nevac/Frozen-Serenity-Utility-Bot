import i18n


async def _help(message, client):
    await message.channel.send(i18n.t('dialogs.help'))
