from configparser import ConfigParser

import i18n

commands = [
    'warning.warning',
    'warning.warnings',
    # 'statistic.giver',
    # 'statistic.taker'
]

config = ConfigParser()
config.read('app.config')
PREFIX = config['Discord']['CommandPrefix']


async def help(message, client):
    dialog = i18n.t('dialogs.help.general')
    dialog += '```' + '\n'.join(
        '\n'.join([
            PREFIX + ' ' + i18n.t('commands.' + cmd).ljust(12) + ' '
            + ' ->'.join(h.ljust(18) for h in help.split('->')) for help in i18n.t('dialogs.help.' + cmd).split(',')
        ])
        for cmd in commands
    ) + '```'
    await message.channel.send(dialog)
