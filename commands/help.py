import i18n


async def help(message, client):
    await message.channel.send(i18n.t('dialogs.help'))
