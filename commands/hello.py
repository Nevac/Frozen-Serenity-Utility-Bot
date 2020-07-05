import i18n


async def hello(message, client):
    await message.channel.send(i18n.t('dialogs.greeting'))
