from commands.help import _help
from exceptions.commandNotFound import CommandNotFound
from services.localizationService import i18n
from commands.warning import warning, warnings

commands = {
    i18n.t('commands.help'): _help,
    i18n.t('commands.warning.warning'): warning,
    i18n.t('commands.warning.warnings'): warnings
}


def resolve_command(input_command):
    command_fragments = input_command.split(' ')

    if len(command_fragments) <= 1:
        return commands[i18n.t('commands.help')]
    else:
        command = command_fragments[1]

        if command in commands.keys():
            return commands[command]
        else:
            raise CommandNotFound
