import i18n


async def unknown(message, client):
    await message.channel.send(i18n.t('dialogs.error.command_not_found'))
